# <codecell>


def createDic4Gid(gid: str):
    return '/{0}/{1}/{2}/{3}'.format(gid[:2],gid[2:4],gid[4:8],gid[8:])

def set_data_path(context, data_dic):
    if context.myself.gid is None:
        raise Exception("Input data_dic is not a node.")
    import os
    path = '/home/gft/work/store' + createDic4Gid(gftIO.gidInt2Str(context.myself.gid))
    os.makedirs(path + "/data", exist_ok=True)
    os.chdir(path)
    
    gftIO.zdump(data_dic,"./data/data.pkl")
    return path



# <codecell>

