
from lib.gftTools import GsEnv
from lib.json_requests import view_data
import datetime
from lib.gftTools import gsUtils
from lib.gftTools.data.j_dict import AllJMap

import time

import numpy as np
import pandas as pd
from lib.gftTools.proto import hbaseTable_pb2
from datetime import date, datetime
from lib.gftTools import gftIO

gsEnv = GsEnv.GsEnv('SHENBIN', 'gft', 'q.gftchina.com', 13567)
# gsEnv = GsEnv.GsEnv('liuqun', 'gft', '192.168.1.166', 9080)
#start connect and login
gsEnv.start()
gsEnv.list_all_agent_links()
gsEnv.join_group_by_index(5)

gsEnv.openTask("5A6BD45239DC4F90BC88220AFCEBC57C")
p = gsEnv.get_policy("5A6BD45239DC4F90BC88220AFCEBC57C", True)

all_j_map = AllJMap.get_map()


from datetime import date, datetime
import pytz

ts_begin = datetime(2016, 12, 31, 0, 0)
ts_end = datetime(2018,1,1,0,0)

start = time.time()
gsEnv.client.get_table_from_hbase("C07FAD50BCF1A5E3B410177656B3A67F", ts_begin, ts_end)
print("read table cost:" + str(time.time()-start))

tab = GsEnv.get_max_timestamp_and_dataframe(gsEnv.client.get_table_from_hbase("C07FAD50BCF1A5E3B410177656B3A67F", ts_begin, ts_end))
gsEnv.console_wait()

'''your logic here.....
   if you have a big loop, periodically call this:
   for example:
'''
for i in range(10000):
    tab = GsEnv.get_max_timestamp_and_dataframe(
        gsEnv.client.get_table_from_hbase("C07FAD50BCF1A5E3B410177656B3A67F", ts_begin, ts_end))
    #

    mat = gftIO.convertColumnTabl2Matrix(tab)
    mat.dot(mat.T) # some expensive operations.
    #call this to keep connection alive.
    gsEnv.wait_push_msg(0)




        # create column tables



'''

inOrOut = True
neighbor_infos = gsEnv.client.get_neighbors("1E10EA792DBC94A959A0D34432138EFE","DATAFLOW", inOrOut, 1000)
neighbor_infos = gsEnv.client.get_neighbors("3544C8290EFC41D3A8D098DD2159424D","DATAFLOW", inOrOut, 1000)


for neighbor in neighbor_infos:
    nodeinfo = gsEnv.client.get_one_node(neighbor[1].gid, neighbor[1].mtime)
    if nodeinfo is not None:
        name = gsUtils.find_prop(nodeinfo.node_prop,'_name')
        if name is None:
            name = "name not found"
    else:
        name = "node not found."
    print("edge[{0}], neigbhor node:[{1}]({2})".format(gsUtils.find_prop(neighbor[0].edge_prop, '_gid'),  neighbor[1].gid, name))

node = gsEnv.client.get_one_node('9ED543FB34C3479FFCF18D056E39092B')

server_resp = gsEnv.client.run_skill("766FEA77054B41B68E34573B2A9F215A",{"para":"1E10EA792DBC94A959A0D34432138EFE", "ExpandLevel":9}, 1000)

resp = gsEnv.client.run_skill_get_as_grphas("766FEA77054B41B68E34573B2A9F215A",{"para":"1E10EA792DBC94A959A0D34432138EFE", "ExpandLevel":9}, 1000)

graph = gsEnv.client.get_fi_inputs_graph("1E10EA792DBC94A959A0D34432138EFE")

class nodeAndEdges:
    def __init__(self,node):
        self.node = node
        self.edges = list()
    def add_edge(self,edge):
        self.edges.append(edge)

node_map = dict()
for node in graph.nodeBriefs:
    node_map[node.id] = nodeAndEdges(node)

for edge in graph.edges:


#
import bson
start_id = str(bson.objectid.ObjectId.from_datetime(datetime.datetime(2018,6,1)))
filter = GsEnv.create_log_filter(start_id, 100, 'DA9E74C09AC8423E96E7986B68B0C4D0')
gsEnv.client.query_log(filter)

#
#
# old api.
gsEnv.view_data( '1852BAEA169AD4633677B8F3E1FB1A6D', '2015-01-01', '2017-08-26', None,
                                             "C459D96A109546D590F014EB1F5A3368",100)


'''
