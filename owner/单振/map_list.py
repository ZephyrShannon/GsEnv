# <codecell>

import numpy as np
import pandas as pd

def map_list(context,gs_func_lambda, gs_list, take_place, args):
    arg_len = len(args)
    if arg_len < (take_place - 1):
        raise Exception("Not enough args for take_place.")
    index = take_place + 1
    ret_list = list()
    for arg in gs_list:
        new_args = args.insert(index, arg)
        ret_list.append(gs_func_lambda.call(*new_args))
    return ret_list

