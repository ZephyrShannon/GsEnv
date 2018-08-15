# <codecell>

from lib.gftTools import gftIO

# test fetch graph
prod_url = 'http://172.16.103.106:9080'
test_user_name = 'wuwei'
test_pwd = 'gft'
gs_call = gftIO.GSCall(prod_url, test_user_name, test_pwd)


def skill_to_graph_node_gid(skill_inst_gid ,key ,key_string ,target_key):
    """ extract skill instance and get graph nodes gid
    1. extract skill instance to get graph
    2. parse graph to get nodes gid
    graph structure:
    graphs {
      graph {
        nodes {
          node_prop {
            props {
              entries {
                key: "_gid"
                value: "D39BB7BF0E3FFEB5CC8E4135EA9D5ED4"
              }
              entries {
                key: "_type"
                value: "readonlyDoc"
              }
              entries {
                key: "url"
                value: "https://zh.wikipedia.org/wiki/%E6%B1%89%E5%A0%A1%E8%AF%81%E5%88%B8%E4%BA%A4%E6%98%93%E6%89%80"
              }
            }
          }
        }
      }
    }
    Keyword Arguments:
    skill_gid  -- skill instance gid
    key        -- source key
    key_string -- source key value
    target_key -- target key
    """
    graph = gs_call.get_graph_from_neo4j(skill_inst_gid)
    ls_extract = []
    for g in graph.graphs:
        dict_node = {}
        for i in g.graph.nodes:
            # print(i.node_prop.props.entries)
            for e in i.node_prop.props.entries:
                dict_node[e.key] = e.value
                # print(dict_node)
            if dict_node[key] == key_string:
                ls_extract.append(dict_node[target_key])
    return ls_extract



# <codecell>

