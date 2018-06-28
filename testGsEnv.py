from lib.gftTools import GsEnv
from lib.json_requests import view_data
import datetime
from lib.gftTools import gsUtils


gsEnv = GsEnv.GsEnv('SHANZ', 'gft', 'q.gftchina.com', 13567)
# gsEnv = GsEnv.GsEnv('SHANBIN', 'gft', '192.168.1.140', 9030)

gsEnv.start()
gsEnv.list_all_agent_links()

gsEnv.join_group_by_index(14)
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
# #
# gsEnv.join_group("60F6058194294084B44C2FFEC9E70233","9887E4EAD9314259A956FE316BB3CB03")
#
# gsEnv.message_loop(60)

resp = gsEnv.openTask("7DE655D204304A52A1A4DB13A49DC191")
policy = gsEnv.get_policy("7DE655D204304A52A1A4DB13A49DC191",True)

#
#
#
gsEnv.view_data( '1852BAEA169AD4633677B8F3E1FB1A6D', '2015-01-01', '2017-08-26', None,
                                             "C459D96A109546D590F014EB1F5A3368",100)

