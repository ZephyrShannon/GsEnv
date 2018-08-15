# <codecell>

import numpy as np
import pandas as pd

# <codecell>


def for_loop(apply_func ,merge_func ,iterators):
    X_iterator = iterators[0]
    y_iterator = iterators[1]
    ret_dict = dict()
    while X_iterator.has_next():
        X_set = X_iteartor.next()
        y     = y_iterator.next()
        na_droped = pd.DataFrame(np.column_stack((X_set, y))).dropna(axis=0,how='any')
        X_set_size = X_set.shape[1]
        X_set_na_droped = na_droped[list(range(X_set_size))]
        y_set_na_droped = na_droped[X_set_size]
        it_ret = apply_func(X_set_na_droped, y_set_na_droped)
        if merge_func is not None:
            it_ret = merge_func(X_iteartor.columns(), it_ret)
        ret_dict[y_iterator.key()] = it_ret
    for it in iterators:
        it.reset()
    if merge_func is not None:
        ret = merge_func(iterators, ret_dict)
        return ret
    return ret_dict

        

# <codecell>

