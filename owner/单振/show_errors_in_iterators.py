# <codecell>




def show_errors_in_iterators(start_index ,end_index ,iterator):
    if end_index is None or end_index < 0:
        end_index = 1000000
    if start_index is None or start_index < 0:
        start_index = 0
    index = 0
    ret_dict = dict()
    error_count = 0
    while iterator.has_next():
        if start_index <= index < end_index:
            val = iterator.next()
            if isinstance(val, gsUtils.ItContinue):
                if error_count <= 20:
                    key = "{0}[{1}]".format(str(iterator.key()),str(index))
                    err_msg = str(val.reason)
                    ret_dict[key] = err_msg
                error_count += 1
        index += 1
    ret_dict['row_count'] = index
    ret_dict['error_count'] = error_count
    return ret_dict


# <codecell>

