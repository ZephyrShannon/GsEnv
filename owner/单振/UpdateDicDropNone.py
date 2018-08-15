# <codecell>


def UpdateDicDropNone(name ,data ,last_dic):
    if last_dic is None:
        last_dic = dict()
    else:
        last_dic = last_dic.copy()
    if data is None:
        return last_dic
    last_dic[name] = data
    return last_dic


# <codecell>

