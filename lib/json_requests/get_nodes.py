import json
from lib.gftTools.gsUtils import str2datetime
from lib.gftTools.proto import common_pb2
MAIN_REQ_NO = 2
SUB_REQ_NO = 2

def create_get_nodes_reqs(node_gid):
    get_node_template = '''{"get_only":1,"node_info":{"box_flag":0,"edges_stat":[],"loc":0,"nid":0,"props":{"_gid":"%s"}}}'''
    req_template = '''{"reqs":[]}'''
    req_json_list = list(['{"reqs":['])
    one_node = get_node_template % (node_gid)
    req_json_list.append(one_node)
    req_json_list.append(']}')
    return ''.join(req_json_list)


from datetime import datetime

def get_nodes_protobuf(resp_body):
    resp_json = resp_body.decode()
    nodes = json.loads(resp_json)
    nodes_map = dict()
    for node in nodes['nodes']:
        proto_node = common_pb2.NodeInfo()
        proto_node.loc = 0
        proto_node.nid = node['nid']
        box_flag = node.get('box_flag')
        if isinstance(box_flag, int):
            proto_node.box_flag = box_flag
        else:
            proto_node.box_flag = 0
        for edge in node['edges_stat']:
            proto_edge = proto_node.edges_stat.add()
            proto_edge.edge_type = edge['e']
            in_val = edge.get('in')
            if in_val is not None:
                proto_edge.__setattr__('in', in_val)
            out_val = edge.get('out')
            if out_val is not None:
                proto_edge.out = out_val
            sub_type = edge.get('subType')
            if sub_type is not None:
                proto_edge.edge_type = sub_type
        gid = None
        mtime = None
        ctime = None
        for key,value in node['props'].items():
            entry = proto_node.node_prop.props.entries.add()
            entry.key = key
            entry.value = value
            if key == '_gid':
                gid = value
            elif key == '_mtime':
                mtime = value
            elif key == '_ctime':
                ctime = value

        if mtime is None:
            if ctime is not None:
                mtime = ctime

        dt = None
        if mtime is None:
            try:
                dt = str2datetime(mtime)
            except ValueError as e:
                print(str(e))

        if dt is None:
            dt = datetime.now()

        nodes_map[gid] = (dt, proto_node)
    return nodes_map

