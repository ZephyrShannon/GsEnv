# <codecell>

def create_dict_using_gid_as_key(context,*args):
    gidList = context.input_list
    result = []
    if len(gidList) != len(args):
        raise Exception("gid list and input have different length")
    for i in range(len(gidList)):
        gid = gftIO.gidInt2Str(gidList[i].gid)
        result.append((gid, args[i]))
    return result    
