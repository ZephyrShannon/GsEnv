import asyncio
from lib.gftTools import gftIO
from lib.gftTools.proto import agentAndAction_pb2

from lib.gftTools.proto.requests_pb2 import EfuRequest, Request

import pandas as pd

from lib.gftTools.proto.responses_pb2 import Message2Client

from lib.gftTools.proto import agentAndAction_pb2
from lib.gftTools.proto import policyTree_pb2

from lib.gftTools.proto import hbaseTable_pb2

from lib.json_requests import view_data

from lib.gftTools import  gsUtils
from lib.json_requests import run_skill
import pymongo
import datetime

import json

import urllib

try:
    import asyncio
    from asyncio import iscoroutine
    from asyncio import Future
except ImportError:
    # Trollius >= 0.3 was renamed
    # noinspection PyUnresolvedReferences
    import trollius as asyncio
    from trollius import iscoroutine
    from trollius import Future

if hasattr(asyncio, 'ensure_future'):
    ensure_future = asyncio.ensure_future
else:  # Deprecated since Python 3.4.4
    ensure_future = asyncio.async

from autobahn.asyncio.websocket import WebSocketClientProtocol

from autobahn.asyncio.websocket import WebSocketClientFactory

from lib.gftTools.proto import requests_pb2
import datetime
import hashlib


def getEncryptedPwd(date_token: str, raw_pwd: str):
    str_con = date_token + raw_pwd
    m = hashlib.md5()
    m.update(str_con.encode())
    return m.digest().hex().upper()


def has_exception(efu_response):
    return efu_response.common.errorCode != 0 or efu_response.common.HasField("errorMessage")

def print_response_exceptions(resp, message):
    print("{0}, error:{1}, {2}".format(message, str(resp.common.errorCode),resp.common.errorMessage))


def create_log_filter(start_id, limit, agent_link=None, group_gid=None, task_gid=None):
    filter = agentAndAction_pb2.SARFilterConditions()
    filter.startId = start_id
    filter.filterGid = ""
    if limit > 10000:
        limit = 10000
    filter.limit = limit
    if agent_link is not None:
        filter.agentLinkGid = agent_link

    if group_gid is not None:
        filter.groupGid = group_gid

    if task_gid is not None:
        filter.taskGid = task_gid

    return filter




MT_EFU_VIEW = 1
ST_RUN_SKILL = 24


MT_AGENT_ACTIONS = 9
ST_UPDATE_VARIABLE_AND_SAVE_LOG = 1
GET_POLICY_TREE = 6

MT_DATA_VISUALIZATION = 4
ST_GET_ORIG_J_FROM_HBASE = 30


MAIN_TASK_VAR_GID = "E258F454466E4AEC9AF8C3D1589D1BDE"
IN_SKILL_GID = '36C1D27B568344449CDC6EA9E281DFE9'
OUT_SKILL_GID  = "F18E7BFA63364709816887F6EB8AC66C"

def get_table_from_hbase_req_json(table_gid: str, start_date:int, end_date:int):
    req = {"tableGid":table_gid, "startDate":start_date}
    if end_date is not None:
        req["endDate"] = end_date
    return json.dumps(req)

def get_neighbors_req_json(start_gid: str, edge_type: str, inOrOout: bool, limit = 9999):
    paras = {"CircleSkill_Start": start_gid, "edgetype": edge_type}
    if inOrOout:
        skill_gid = IN_SKILL_GID
    else:
        skill_gid = OUT_SKILL_GID
    req_json = run_skill.create_run_skill_para(skill_gid, paras, limit)
    # print(req_json)
    return req_json


class TaskData:
    def __init__(self, gid):
        self.gid = gid
        self.svt = None
        self.action_space = None
        self.policy_tree = None


class GsEnv:
    def __init__(self, user_name, pwd, ip, port, lang='chn'):
        self.loop = asyncio.get_event_loop()
        self.client = GsClient(user_name, pwd, ip, port, lang, self.loop)
        self.cur_agent_link = None

        return

    def start(self):
        self.client.start_login()

    def openTask(self, task_gid:str):
        update = agentAndAction_pb2.UpdateVarAndSaveLog()
        if (self.cur_agent_link is None):
            print("Join group first!")
            return
        update.agentLink = self.cur_agent_link
        update.forTaskGid = task_gid
        col = update.agentLinkVars.add()
        col.stateVariable = MAIN_TASK_VAR_GID
        one_val = col.cells.add()
        one_val.gid = task_gid
        resp = self.client.send_req(MT_AGENT_ACTIONS, ST_UPDATE_VARIABLE_AND_SAVE_LOG, update.SerializeToString(), 3000)
        if has_exception(resp):
            print("Exception[" + str(resp.common.errorCode) + "]:" + resp.common.errorMessage)
            print("Open task failed!")
        else:
            print("Task[{0}] opened, svt and policy will received later".format(task_gid))
        return resp

    def get_policy(self, task_gid, reload):
        if self.cur_agent_link is None:
            print("Join group first!")
            return
        req = policyTree_pb2.OpenPolicyTreeRequest()
        req.taskInstGid = task_gid
        req.agentLinkGid = self.cur_agent_link
        req.loadPolicyTree = reload
        req.getBuilderUI = False
        resp = self.client.send_req(MT_AGENT_ACTIONS, GET_POLICY_TREE, req.SerializeToString(), 15000)
        if has_exception(resp):
            print("Get policy of task[{0}] failed".format(task_gid))
            return None
        else:
            print("Policy get!")
            resp_policy = policyTree_pb2.OpenPolicyTreeResponse()
            resp_policy.ParseFromString(resp.body)
            return resp_policy

    def message_loop(self, timeout_sec=10):
        print("Start waiting")
        push_msg = self.wait_push_msg(timeout_sec)
        if push_msg is None:
            print("Time out and returned.")
        elif isinstance(push_msg, DisconEvent):
            print("Find disconnect, code:" + str(push_msg.code) + ", reason:" + str(push_msg.reason))
        else:
            self.apply_push_msg(push_msg)

    def apply_push_msg(self, push_msg):
        if push_msg.HasField("updateVarAndLog") and push_msg.updateVarAndLog.HasField("agentLinkVars"):
            self.client.update_state_var(push_msg.updateVarAndLog.agentLinkVars)
        elif push_msg.HasField("transcation"):
            self.client.update_qcoin(push_msg.transcation)

    def list_all_agent_links(self):
        index = 1
        for group, agent_service in self.client.group_agent_service_list:
            print(str.format("{4}:Group:{0}[{1}], agentLink:{2}[{3}]", gsUtils.get_property(group, '_name'),gsUtils.get_property(group, '_gid'),
                             gsUtils.get_property(agent_service, '_name'), gsUtils.get_property(agent_service, '_gid'),str(index)))
            index = index + 1

    '''
    overwrite this function. 
    first join group, use self.client.group_agent_service_list. or self.client.recommand_groups
    '''
    def join_group_by_index(self, index):
        group, agent_service = self.client.group_agent_service_list[index-1]
        self.join_group(gsUtils.get_property(group, '_gid'), gsUtils.get_property(agent_service, '_gid'))


    def join_group(self, group_gid, agent_link_gid):
        # join group.
        group = self.client.join_group_as_agent_service(group_gid, agent_link_gid)
        if group is not None:
            self.cur_agent_link = agent_link_gid

    def __waiting_fut__(self, msg_fut: Future, timeout_sec):
        try:
            self.loop.run_until_complete(asyncio.wait_for(msg_fut, timeout_sec, loop=self.loop))
        except asyncio.TimeoutError:
            return None
        except DisconEvent as event:
            return event
        return msg_fut.result()

    def wait_push_msg(self, timeout_sec=100):
        push_msg_fut = asyncio.Future()
        self.client.push_future = push_msg_fut
        return self.__waiting_fut__(push_msg_fut, timeout_sec)

    def view_data(self, gid, time_begin, time_end, write2file, calc_server_gid, timeout_sec):
        if isinstance(time_begin, str):
            time_begin = pd.Timestamp(time_begin)
        print(str(type(time_begin)))
        if isinstance(time_end, str):
            time_end = pd.Timestamp(time_end)
        req = view_data.create_view_data_req(gid, time_begin, time_end, write2file, calc_server_gid)
        efu_req = self.client.wrapper_up_request(4, 5, req, timeout_sec)
        return self.client.sync_send_req(efu_req.SerializeToString(), efu_req.efuRequest.common.requestNo, timeout_sec)


from lib.gftTools import gsUtils
import zlib
import json


class DisconEvent(Exception):
    def __init__(self, wasClean, code, reason):
        self.wasClean = wasClean
        self.code = code
        self.reason = reason



def get_max_timestamp_and_dataframe(tab:hbaseTable_pb2.HBaseTable):
    col_len = tab.rows.__len__()
    all_cols = list()
    for i in range(tab.meta.oSize + tab.meta.tSize + tab.meta.vSize):
        all_cols.append(list())
    for row in tab.rows:
        idx = 0
        for o in row.o:
            all_cols[idx].append(o)
            idx += 1

        for t in row.t:
            all_cols[idx].append(t)
            idx += 1

        for v in row.v:
            all_cols[idx].append(v)
            idx += 1

    d = dict()
    idx = 0
    for name in tab.meta.column_names:
        d[name] = all_cols[idx]
        idx += 1
    df = pd.DataFrame(d, columns=tab.meta.column_names)

    idx = tab.meta.oSize
    for i in range(tab.meta.tSize):
        name = tab.meta.column_names[i + idx]
        df[name] = pd.to_datetime(df[name], unit='ms')   #.dt.tz_localize('Asia/Shanghai')
    df.last_update_ts = tab.meta.updateTimestamp
    return df

class GsClient(WebSocketClientProtocol):
    def __init__(self, user, pwd, ip, port, lang, loop):
        super().__init__()
        self.user = user
        self.lang = lang
        self.pwd = pwd
        self.req_no = 0
        self.req_map = dict()
        self.closed = True
        ws_url = str.format("ws://{0}:{1}/vqservice/vq/socket", ip, str(port))
        self.ws_url = ws_url
        self.ip = ip
        self.port = port
        self.factory = WebSocketClientFactory(ws_url)
        self.factory.protocol = lambda: self
        self.loop = loop
        self.push_future = None
        self.group_agent_service_list = list()  # list of tuple (group_gid, agent_service) //all the group that is arleady joined
        self.recommand_groups = list()  #
        self.state_vars = dict()  # {group:{agent_servic:{var_name:var_value}}}
        self.node_caches = dict()  # gid->(date, nodeInfo)
        self.joined_group_and_agent_service = list()
        # import sqlite3
        # self.conn = sqlite3.connect('nodes.db')

    # def get_node_info(self, gid: str):
    #     cursor = self.conn.execute(str.format("SELECT * FROM nodes where g='{0}", gid))
    #     return cursor.fetchone()




    def set_stat_var(self, group_gid, node_gid, var_name, var):
        agent_service_dict = self.state_vars.get(group_gid)
        if agent_service_dict is None:
            agent_service_dict = dict()
            self.state_vars[group_gid] = agent_service_dict

        var_name_dict = agent_service_dict.get(node_gid)
        if var_name_dict is None:
            var_name_dict = dict()
            agent_service_dict[node_gid] = var_name_dict
        var_name_dict[var_name] = var

    def update_state_var(self, update_cols):
        pass
        # for col in update_cols:
        #     self.set_stat_var(updates.group, updates.agentLink, var.nameGid, var)

    def update_qcoin(self, trans):
        if trans.HasField("userId"):
            if trans.userId != self.user_id:
                print("Get update of other user:[" + trans.userId + "]")
                return
        self.qcoin = trans.qCoinNow

    def get_state_var(self, group_gid, agent_service_gid, var_name):
        agent_service_dict = self.state_vars.get(group_gid)
        if agent_service_dict is None:
            return None
        var_name_dict = agent_service_dict.get(agent_service_gid)
        if var_name_dict is None:
            return None
        return var_name_dict.get(var_name)

    def on_quit_group(self, group_gid):
        if self.state_vars.__contains__(group_gid):
            self.state_vars.pop(group_gid)

    #return a list of edge, node_brief
    def get_neighbors(self, my_gid, edge_type, inOrOut, limit):
        req_json = get_neighbors_req_json(my_gid, edge_type, inOrOut, limit)
        resp = self.send_req(run_skill.MAIN_REQ_NO, run_skill.SUB_REQ_NO, req_json, 100)
        if has_exception(resp):
            print_response_exceptions(resp, "Get neighbor failed,")
            return None
        else:
            neighbor_graph = run_skill.get_first_graph(run_skill.paser_resp_actions(resp.body))
            if neighbor_graph is None:
                return list()
            node_brief_map = dict()
            for node in neighbor_graph.nodeBriefs:
                node_brief_map[node.id] = node

            list_edge_tuple = list()
            for edge in neighbor_graph.edges:
                if inOrOut:
                    node_brief = node_brief_map.get(edge.sn_id)
                else:
                    node_brief = node_brief_map.get(edge.en_id)
                list_edge_tuple.append((edge, node_brief))
            return list_edge_tuple

    def run_skill(self, skill_gid, skill_paras:dict, limit:int):
        req_json = run_skill.create_run_skill_para(skill_gid, skill_paras, limit)
        resp = self.send_req(run_skill.MAIN_REQ_NO, run_skill.SUB_REQ_NO, req_json, 100)
        if has_exception(resp):
            print_response_exceptions(resp, "Run skill failed,")
            return None
        else:
            return resp



    def get_table_from_hbase(self, table_gid, start_date, end_date):
        ''' return a table defined in HBaseTable'''
        if isinstance(start_date, datetime.datetime):
            start_date = int(start_date.timestamp() * 1000)
        if isinstance(end_date, datetime.datetime):
            end_date = int(end_date.timestamp() * 1000)
        req_json = get_table_from_hbase_req_json(table_gid, start_date, end_date)
        print("send request json:"+ req_json)
        resp = self.send_req(MT_DATA_VISUALIZATION, ST_GET_ORIG_J_FROM_HBASE, req_json, 100)
        if has_exception(resp):
            print_response_exceptions(resp, "Get table from hbase failed,")
            return None
        else:
            table = hbaseTable_pb2.HBaseTable()
            table.ParseFromString(resp.body)
            return table


    def run_skill_get_as_grphas(self, skill_gid, skill_paras:dict, limit:int):
        server_resp = self.run_skill(skill_gid, skill_paras, limit)
        if server_resp is not None:
            return run_skill.get_all_graph(run_skill.paser_resp_actions(server_resp.body))
        else:
            return None

    def get_fi_inputs_graph(self, fi_gid):
        graph_list = self.run_skill_get_as_grphas("766FEA77054B41B68E34573B2A9F215A",{"para":fi_gid, "ExpandLevel":99}, 1000)
        if graph_list is not None and graph_list.__len__() == 1:
            return graph_list[0]
        return None

    def get_one_node(self, node_gid, mtime_str = None):
        if mtime_str is not None:
            try:
                mtime = gsUtils.str2datetime(mtime_str)
            except ValueError as e:
                print(str(e))
                mtime = None
        else:
            mtime = None

        ret = self.node_caches.get(node_gid)
        if (mtime is not None) and (ret is not None):
            if ret[0] < mtime:
                ret = None

        if ret is None:
            nodes_map = self.__read_nodes_from_server__(node_gid)
            ret = nodes_map.get(node_gid)
            if (ret is not None):
                self.node_caches.__setitem__(node_gid, ret)
        return ret[1]

    def __read_nodes_from_server__(self, node_gid):
        from lib.json_requests import get_nodes
        req_json = get_nodes.create_get_nodes_reqs(node_gid)
        resp = self.send_req(get_nodes.MAIN_REQ_NO, get_nodes.SUB_REQ_NO, req_json, 100)
        if has_exception(resp):
            print_response_exceptions(resp, "Get nodes failed,")
            return None
        return get_nodes.get_nodes_protobuf(resp.body)

    def init_common(self, common):
        common.product = "openAIEnv"
        common.version = '1.0.0'
        common.language = 'chn'
        common.requestNo = self.getReqNo()

    def wrapper_up_request(self, main_req_no, sub_req_no, req_data, timeout_sec):
        req = requests_pb2.Request()
        self.init_common(req.efuRequest.common)
        req.efuRequest.mainRequestNo = main_req_no
        req.efuRequest.subRequestNo = sub_req_no
        req.efuRequest.token = self.token
        req.efuRequest.timeoutMs = timeout_sec * 1000
        if isinstance(req_data, dict):
            req.efuRequest.isBytes = False
            request_bytes = json.dumps(req_data).encode('utf-8')
        elif isinstance(req_data, str):
            req.efuRequest.isBytes = False
            request_bytes = req_data.encode('utf-8')
        else:  # assuming this is protobuf data
            req.efuRequest.isBytes = True
            request_bytes = req_data
        req.efuRequest.isCompressed = True
        orig_len = len(request_bytes)
        request_bytes = zlib.compress(request_bytes, 5)
        req.efuRequest.noEncryption = True
        req_len = len(request_bytes)
        ret = bytearray(req_len + 4)
        len_bytes = orig_len.to_bytes(4, 'big')
        for i in range(4):
            ret[i] = len_bytes[i]
        for i in range(req_len):
            ret[i + 4] = request_bytes[i]
        req.efuRequest.body = bytes(ret)
        req.efuRequest.crc32 = 0
        return req

    def send_req(self, main_req_no, sub_req_no, req_data, timeout_sec):
        efu_req = self.wrapper_up_request(main_req_no, sub_req_no, req_data, timeout_sec)
        return self.sync_send_req(efu_req.SerializeToString(), efu_req.efuRequest.common.requestNo, timeout_sec)

    def unwrapper_response(self, efu_response):
        if efu_response.HasField('body'):
            if efu_response.isCompressed:
                efu_response.body = zlib.decompress(efu_response.body[4:])
        return efu_response

    '''
    :parameter group_gid, if None, than will create a new one.
    '''

    def join_group_as_agent_service(self, group_gid=None, agent_link_gid=None):
        print("Join group now!")
        if (group_gid is None):
            for group, agent_service in self.group_agent_service_list:
                group_gid = gsUtils.get_property_in_nodeinfo(group, '_gid')
                agent_link_gid = gsUtils.get_property_in_nodeinfo(agent_service, '_gid')
                break

        join_group = agentAndAction_pb2.JoinGroup()
        join_group.groupGid = group_gid
        join_group.copy = False
        join_group.reuseOldAgentLink = agent_link_gid
        efu_req = self.wrapper_up_request(9, 3, join_group.SerializeToString(), 100)
        resp = self.sync_send_req(efu_req.SerializeToString(), efu_req.efuRequest.common.requestNo)
        if (not has_exception(resp)):
            new_group = agentAndAction_pb2.NewGroupInfo()
            new_group.ParseFromString(resp.body)
            group_gid = gsUtils.get_property_in_nodeinfo(new_group.group, "_gid")
            agent_service_gid = gsUtils.get_property_in_nodeinfo(new_group.myAgentLink.agentLink, "_gid")
            print("Group:" + gsUtils.get_property_in_nodeinfo(new_group.group, "_name") + "joined:")
            self.joined_group_and_agent_service.append((new_group.group, new_group.myAgentLink.agentLink))

            if new_group.HasField('groupSvt'):
                self.update_state_var(new_group.svt.columns)
            return new_group
        else:
            print("Exception[" + str(resp.common.errorCode) + "]:" + resp.common.errorMessage)
        return None

    def start_login(self):
        coro = self.loop.create_connection(self.factory, self.ip, self.port)
        self.loop.run_until_complete(coro)
        self.connnection_done = asyncio.Future()
        connected = self.loop.run_until_complete(self.connnection_done)
        print("Start login!")
        if connected:
            self.send_hello()
            return True
        else:
            return False

    def getReqNo(self):
        self.req_no = self.req_no + 1
        return self.req_no

    def sendReq(self, req_data, req_no):
        future = asyncio.Future()

        self.req_map[req_no] = future
        self.sendMessage(payload=req_data, isBinary=isinstance(req_data, bytes))
        return future

    def sync_send_req(self, req_data, req_no, timeout_sec=300):
        ft = self.sendReq(req_data, req_no)
        try:
            self.loop.run_until_complete(asyncio.wait_for(ft, timeout_sec, loop=self.loop))
        except asyncio.TimeoutError:
            return None
        except DisconEvent as ev:
            return None
        return ft.result()

    def send_hello(self):
        print("Login sent")
        login = requests_pb2.Request()
        login.loginRequest.user = self.user
        login.loginRequest.datetime = str(datetime.datetime.now())
        self.init_common(login.loginRequest.common)
        login.loginRequest.password = getEncryptedPwd(login.loginRequest.datetime, self.pwd)
        resp = self.sync_send_req(login.SerializeToString(), login.loginRequest.common.requestNo, 30)
        # resp = await self.sendReq(login.SerializeToString(), login.loginRequest.common.requestNo)
        print("Message send!")
        self.onLoginResp(resp)

    def onLoginResp(self, login_resp):
        print("Resp common:" + str(login_resp.common))
        if login_resp.common.errorCode == 0:
            self.user_id = login_resp.userId
            self.token = login_resp.token
            self.name = login_resp.userName
            self.qcoin = 0
            # if login_resp.HasField('account'):
            #     self.qcoin = login_resp.account.qCoin
            # else:
            #     self.qcoin = 0

            for pair in login_resp.allAgentLinks:
                self.group_agent_service_list.append((pair.group, pair.agentLink))

            for group in login_resp.groups:
                self.group_agent_service_list.append(group)

            print("Login success")
        else:
            self.sendClose(0, "Pwd incorrect.")
            print("Login failed")

    def onOpen(self):
        print("On opened")
        self.closed = False
        self.connnection_done.set_result(True)
        self.connnection_done = None


    def query_log(self, filter):
        efu_req = self.wrapper_up_request(9, 11, filter.SerializeToString(), 100)
        resp = self.sync_send_req(efu_req.SerializeToString(), efu_req.efuRequest.common.requestNo)
        if (not has_exception(resp)):
            logs = agentAndAction_pb2.UpdateVarAndSaveLog()
            logs.ParseFromString(resp.body)
            return logs.actions
        else:
            print("Exception[" + str(resp.common.errorCode) + "]:" + resp.common.errorMessage)
        return None


    def on_push_msg(self, msg):
        if self.push_future is not None:
            self.push_future.set_reuslt(msg)

    def onMessage(self, payload, is_binary):
        if is_binary:
            resp = Message2Client()
            resp.ParseFromString(payload)
            if resp.HasField("loginResponse"):
                future = self.req_map.pop(resp.loginResponse.common.requestNo, None)
                if future is not None:
                    future.set_result(resp.loginResponse)
                return
            elif resp.HasField("efuResponse"):
                print("Get resp of:" + str(resp.efuResponse.common.requestNo) + "len:" + str(
                    len(payload)) + " type:" + str(resp.efuResponse.mainRequestNo) + ":" + str(
                    resp.efuResponse.subRequestNo))
                future = self.req_map.pop(resp.efuResponse.common.requestNo, None)
                if future is not None:
                    future.set_result(self.unwrapper_response(resp.efuResponse))
                return
            else:
                return self.on_push_msg(resp)
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        self.closed = True
        print("Connection closed!")
        if self.connnection_done is not None:
            self.connnection_done.set_result(False)
            self.connnection_done = None
        dis_event = DisconEvent(wasClean, code, reason)
        if self.push_future is not None:
            self.push_future.set_exception(dis_event)
        for ft in self.req_map.values():
            ft.set_exception(dis_event)
        self.req_map.clear()

    async def wait(self):
        if self.closed:
            await asyncio.sleep(1)

            #
            # gsEnv = GsEnv('SHANZ', 'gft', '192.168.1.140', 9030)
            #
            # gsEnv.start()
