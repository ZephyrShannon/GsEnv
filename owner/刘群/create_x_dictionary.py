# <codecell>




def create_x_dictionary(context, *args):
    gidList = context.input_list
    dic = {}
    if len(gidList) != len(args):
        raise Exception("gid list and input have different length")
    for i in range(len(gidList)):
        gid = gftIO.gidInt2Str(gidList[i].gid)
        dic[gid] = args[i]
    return dic


# <codecell>

