# <codecell>

import pandas as pd


def dict_to_nonsymbol(iterator):
    index = list()
    data = list()
    while iterator.has_next():
        val = iterator.next()
        f_val = float(val)
        data.append(f_val)
        index.append(iterator.key())
        
    columns = [gftIO.gid_str_to_bin('00000000000000000000000000000000')]
    return pd.DataFrame(data=data,index=index,columns=columns)

        


# <codecell>

