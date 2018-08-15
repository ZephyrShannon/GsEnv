# <codecell>

import numpy as np
import pandas as pd

# <codecell>




def for_loop(apply_func ,iterator):
    ret_dict = dict()
    while iterator.has_next():
        data = iterator.next()
        if data is not None:
            ret = apply_func(data)
            ret_dict[iterator.key()] = ret
        else:
            ret_dict[iterator.key()] = None
    iterator.reset()
    return gsUtils.DictIterator(ret_dict)


# <codecell>

