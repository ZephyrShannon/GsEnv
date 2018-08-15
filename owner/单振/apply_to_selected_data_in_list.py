# <codecell>

import pandas as pd
import numpy as np


reform_all_index_and_columns = 5
reform_index_and_one_columns = 4
reform_columns_and_one_index = 3
reform_only_index = 2
reform_only_columsn = 1
reform_not_available = 0

def check_is_orig_df(ret, orig_df):
    if orig_df.ndim == 2:
        if orig_df.shape[0] == ret.shape[0]:
            if orig_df.shape[1] == ret.shape[1]:
                return reform_all_index_and_columns
            elif ret.shape[1] == 1:
                return reform_index_and_one_columns
            else:
                return reform_only_index  # continue checking more inputs
        elif orig_df.shape[1] == ret.shape[1]:
            if ret.shape[0] == 1:
                return reform_columns_and_one_index
            else:
                return reform_only_columsn
    return reform_not_available


def apply_to_selected_data_in_list(apply_func ,apply_indexes ,append_result_at_tail, *iterators):
    indexes = apply_indexes.split(',')
    indexes = set(map(lambda x: int(x), indexes))

    iterator_list = gsUtils.prepare_iterator(*iterators)
    available_it = iterator_list[0]
    ret_dict = dict()
    data_list = list()
    check_for_df = True
    reform_df = 0
    orig_data_index = 0
    all_none = True
    selected_data_list = list()
    while available_it.has_next():
        skip_row = None
        data_list.clear()
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
            ret_list = list()
            input_range = range(len(data_list))
            selected_data_list.clear()
            for i in input_range:
                data = data_list[i]
                if indexes.__contains__(i):
                    selected_data_list.append(data)
                else:
                    ret_list.append(data)

            one_ret = apply_func(*selected_data_list)
            try:
                pass
            except Exception as e:
                reason = 'Key:' + str(available_it.key()) + " error:" + str(e)
                one_ret = gsUtils.ItContinue(reason)
                

            if check_for_df:
                if not isinstance(one_ret, gsUtils.ItContinue):
                    check_for_df = False
                    if isinstance(one_ret, np.ndarray) and one_ret.ndim == 2:
                        for i in input_range:
                            data = selected_data_list[i]
                            if isinstance(data, pd.DataFrame):
                                reform_df = check_is_orig_df(one_ret, data)
                                if (reform_df > 0):
                                    orig_data_index = i
                                    break;
                        #             if apply_func.func_gid == '4D78A6E3FE645AF5C97F9A92B8310289':
                        #                 raise Exception("reform_df:{0}, idx:{1}".format(str(reform_df),str(using_df_idx)))
            if reform_df > 0:
                orig_data = selected_data_list[orig_data_index]
                if reform_df == reform_all_index_and_columns:
                    one_ret = pd.DataFrame(data=one_ret, index=orig_data.index, columns=orig_data.columns)
                elif reform_df == reform_index_and_one_columns:
                    one_ret = pd.DataFrame(data=one_ret, index=orig_data.index, columns=['result'])
                elif reform_df == reform_columns_and_one_index:
                    one_ret = pd.DataFrame(data=one_ret, index=['result'], columns=orig_data.columns)
                elif reform_df == reform_only_index:
                    one_ret = pd.DataFrame(data=one_ret, index=orig_data.index)
                else:
                    one_ret = pd.DataFrame(data=one_ret, columns=orig_data.columns)

            if append_result_at_tail:
                ret_list.append(one_ret)
            else:
                ret_list.insert(0, one_ret)
        else:
            ret_list = skip_row
        ret_dict[available_it.key()] = ret_list
    # for it in iterator_list:
    #     it.reset()
    if all_none:
        raise Exception("All input data is None for func:" + apply_func.func_gid)
    ret = gsUtils.create_dict_iterator(ret_dict)
    ret.set_as_list()
    return ret




# <codecell>

