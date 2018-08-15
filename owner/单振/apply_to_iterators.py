# <codecell>

import numpy as np
import pandas as pd

# <codecell>

reform_all_index_and_columns = 5
reform_index_and_one_columns = 4
reform_columns_and_one_index = 3
reform_only_index = 2
reform_only_columsn = 1

def for_loop(apply_func, ret_as_list, *iterators):
    iterator_list = gsUtils.prepare_iterator(*iterators)
    available_it = iterator_list[0]
    ret_dict = dict()
    data_list = list()
    check_for_df = True
    reform_df = 0
    using_df_idx = 0
    all_none = True
    while available_it.has_next():
        skip_row = None
        for it in iterator_list:
            val = it.next()
            if isinstance(val, gsUtils.ItContinue):
                skip_row = val
                continue
            if it.as_list:
                data_list.extend(val)
            else:
                data_list.append(val)
        if skip_row is None:
            all_none = False
            try:
                ret = apply_func(*data_list)
            except Exception as e:
                reason = 'Key:' + str(available_it.key()) + " error:" + str(e)
                ret = gsUtils.ItContinue(reason)


            if check_for_df:
                if not isinstance(ret, gsUtils.ItContinue):
                    check_for_df = False
                    if isinstance(ret, np.ndarray) and ret.ndim == 2:
                        for i in range(len(data_list)):
                            orig_df = data_list[i]
                            if isinstance(orig_df, pd.DataFrame):
                                if orig_df.ndim ==  2:
                                    using_df_idx = i
                                    if orig_df.shape[0] == ret.shape[0]:
                                        if orig_df.shape[1] == ret.shape[1]:
                                            reform_df = reform_all_index_and_columns
                                            break;
                                        elif ret.shape[1] == 1:
                                            reform_df = reform_index_and_one_columns
                                            break;
                                        else:
                                            reform_df = reform_only_index # continue checking more inputs
                                    elif orig_df.shape[1] == ret.shape[1]:
                                        if ret.shape[0] == 1:
                                            reform_df = reform_columns_and_one_index
                                            break;
                                        else:
                                            reform_df = reform_only_columsn
#             if apply_func.func_gid == '4D78A6E3FE645AF5C97F9A92B8310289':
#                 raise Exception("reform_df:{0}, idx:{1}".format(str(reform_df),str(using_df_idx)))
            if reform_df > 0:
                orig_df = data_list[using_df_idx]
                if reform_df == reform_all_index_and_columns:
                    ret = pd.DataFrame(data=ret, index=orig_df.index, columns=orig_df.columns)
                elif reform_df == reform_index_and_one_columns:
                    ret = pd.DataFrame(data=ret, index=orig_df.index, columns=['result'])
                elif reform_df == reform_columns_and_one_index:
                    ret = pd.DataFrame(data=ret, index=['result'], columns=orig_df.columns)
                elif reform_df == reform_only_index:
                    ret = pd.DataFrame(data=ret, index=orig_df.index)
                else:
                    ret = pd.DataFrame(data=ret, columns=orig_df.columns)
        else:
            ret = skip_row
        ret_dict[available_it.key()] = ret
        data_list.clear()
    # for it in iterator_list:
    #     it.reset()
    if all_none:
        raise Exception("All input data is None for func:"+apply_func.func_gid)
    ret = gsUtils.create_dict_iterator(ret_dict)
    if ret_as_list:
        ret.set_as_list()
    return ret

"""
def for_loop(apply_func, ret_as_list, *iterators):
    iterator_list = gsUtils.prepare_iterator(*iterators)
    available_it = iterator_list[0]
    ret_dict = dict()
    data_list = list()
    check_for_df = True
    reform_df = 0
    while available_it.has_next():
        skip_row = None
        for it in iterator_list:
            val = it.next()
            if isinstance(val, gsUtils.ItContinue):
                skip_row = val
                continue
            if it.as_list:
                data_list.extend(val)
            else:
                data_list.append(val)
        if skip_row is None:
            ret = apply_func(*data_list)
            if check_for_df:
                if len(data_list) != 1:
                    check_for_df = False
                elif not isinstance(ret, gsUtils.ItContinue):
                    check_for_df = False
                    orig_df = data_list[0]
                    if isinstance(orig_df, pd.DataFrame) and isinstance(ret, np.ndarray):
                        if orig_df.ndim == ret.ndim == 2:
                            if orig_df.shape[0] == ret.shape[0]:
                                if orig_df.shape[1] == ret.shape[1]:
                                    reform_df = reform_all_index_and_columns
                                elif ret.shape[1] == 1:
                                    reform_df = reform_index_and_one_columns
                                else:
                                    reform_df = reform_only_index
                            elif orig_df.shape[1] == ret.shape[1]:
                                if ret.shape[0] == 1:
                                    reform_df = reform_columns_and_one_index
                                else:
                                    reform_df = reform_only_columsn
            if reform_df > 0:
                orig_df = data_list[0]
                if reform_df == reform_all_index_and_columns:
                    ret = pd.DataFrame(data=ret, index=orig_df.index, columns=orig_df.columns)
                elif reform_df == reform_index_and_one_columns:
                    ret = pd.DataFrame(data=ret, index=orig_df.index, columns=['result'])
                elif reform_df == reform_columns_and_one_index:
                    ret = pd.DataFrame(data=ret, index=['result'], columns=orig_df.columns)
                elif reform_df == reform_only_index:
                    ret = pd.DataFrame(data=ret, index=orig_df.index)
                else:
                    ret = pd.DataFrame(data=ret, columns=orig_df.columns)
        else:
            ret = skip_row
        ret_dict[available_it.key()] = ret
        data_list.clear()
    # for it in iterator_list:
    #     it.reset()
    ret = gsUtils.create_dict_iterator(ret_dict)
    if ret_as_list:
        ret.set_as_list()
    return ret

"""


# <codecell>

