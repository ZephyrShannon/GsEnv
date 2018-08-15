# <codecell>

import numpy as np
import pandas as pd

# <codecell>




def loop_of_list_val(apply_func ,iterator):
    ret_dict = dict()
    while iterator.has_next():
        data = iterator.next()
        if data is not None:
            ret = apply_func(*data)
            ret_dict[iterator.key()] = ret
        else:
            ret_dict[iterator.key()] = None
    iterator.reset()
    return gsUtils.DictIterator(ret_dict)

def test_none(it):
    while it.has_next():
        val = it.next()
        if val is not None:
            print("it[{0}] has val of type{1}".format(str(it.key()),str(val)))


# <codecell>

