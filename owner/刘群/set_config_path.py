# <codecell>

def createDic4Gid(gid: str):
    return '/{0}/{1}/{2}/{3}'.format(gid[:2], gid[2:4], gid[4:8], gid[8:])

def set_config_path(context, config_dic):
    if context.myself.gid is None:
        raise Exception("Input data_dic is not a node.")
    import os
    path = '/home/gft/work/store' + createDic4Gid(gftIO.gidInt2Str(context.myself.gid))
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    import json
    with open('pgportfolio/net_config.json','w') as outfile:
        json.dump(config_dic, outfile)

    return path


# <codecell>

