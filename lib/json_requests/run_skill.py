from lib.gftTools import gsUtils
import json
from lib.gftTools.proto import skill_pb2

MAIN_REQ_NO = 1
SUB_REQ_NO = 24

def create_para(key, val, paras_dict):
    val_obj = dict()
    if isinstance(val, str):
        if gsUtils.is_gs_gid(val):
            val_obj['gid'] = val
        else:
            val_obj['val'] = val
    else:
        val_obj['val'] = val
    paras_dict[key] = val_obj


def create_run_skill_para(skill_gid: str, paras: dict, limit):
    json_obj = dict()
    json_obj['gid_n_action'] = skill_gid
    json_obj['verb'] = 'run'
    paras_obj = dict()
    for key, val in paras.items():
        create_para(key, val, paras_obj)

    search_para_obj = dict()
    if isinstance(limit, int):
        search_para_obj['limit'] = limit
    search_para_obj['orderBy'] = -1
    search_para_obj['paras'] = paras_obj
    search_para_obj['respType'] = 1

    skill_para_obj = {"com.gftchina.common.SearchParameters": search_para_obj}

    json_obj['para'] = skill_para_obj
    return json.dumps(json_obj)

def paser_resp_actions(resp_body):
    resp_data = skill_pb2.RespRunNodeActions()
    resp_data.ParseFromString(resp_body)
    return resp_data

def get_first_graph(resp_data):
    if resp_data.resps.__len__() == 1:
        if resp_data.resps[0].graphs.__len__() == 1:
            return resp_data.resps[0].graphs[0].graph
    return None


def get_all_graph(skill_resp_actions):
    ret = list()
    for resp in skill_resp_actions.resps:
        for graph in resp.graphs:
            ret.append(graph.graph)
    return ret
