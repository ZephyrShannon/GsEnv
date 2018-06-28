# -*- coding: utf-8 -*-
from . import gftIO
import numpy as np
import pandas as pd
import xarray

def getCashGid():
    return gftIO.strSet2Np(np.array(['0AC062D610A1481FA5561EC286146BCC']))


def getGodGid():
    return np.chararray(1, itemsize=16, buffer='\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')


def getSingleGodGid():
    iv = 0
    return iv.to_bytes(16,byteorder='little')

def getParm(dict_parm, parmName, defaultValue):
    if parmName in dict_parm:
        return dict_parm[parmName]
    else:
        return defaultValue


def alignDate(sourceDates, targetDates, method='ffill', returnidx=False):
    """
    source dates: rebalance dates
    target dates: all dates
    """

    df_dateMap = pd.DataFrame({'targetDate':targetDates, 'idx':np.arange(len(targetDates))}, index=targetDates)
    if isinstance(sourceDates, pd.Timestamp):
        df_dateMap = df_dateMap.reindex([sourceDates], method=method)
    else:
        df_dateMap = df_dateMap.reindex(sourceDates, method=method)
    if returnidx:
        result = np.array(df_dateMap['idx'])
        if isinstance(sourceDates, pd.Timestamp):
            result = result[0]
    else:
        if isinstance(sourceDates, pd.Timestamp):
            result = df_dateMap['targetDate'][0]
        else:
            if isinstance(sourceDates, pd.DatetimeIndex):
                result = pd.DatetimeIndex(df_dateMap['targetDate'])
            else:
                result = np.array(df_dateMap['targetDate'])
    return result


def roundToLot(sizeArray, lotSize):
    if lotSize > 0:
        sizeArray = sizeArray.fillna(0)
        return np.sign(sizeArray) * lotSize * np.floor(np.round(abs(sizeArray)) / max(1., lotSize))
    else:
        return sizeArray


def cut2bin(ser_x, totalBinNum, ascending=False):
    # calculate bin size
    totalBinNum = int(totalBinNum)
    xlen = len(ser_x)
    arr_binsize = np.repeat(xlen // totalBinNum, totalBinNum)
    remaining = xlen % totalBinNum
    if remaining > 0:
        arr_binsize[:remaining] += 1
    # map each signal to its binIdx
    arr_binmap = np.repeat(np.arange(totalBinNum) + 1, arr_binsize)
    ser_xrank = ser_x.rank(method='first', ascending=ascending)
    ser_result = pd.Series(
        arr_binmap[np.array(ser_xrank.values - 1, dtype='int')])
    return ser_result


class Strategy:
    #hold the strategy result, including cumret, holding
    def __init__(self, gid, cumret, holding):
        # save matrix and column table.
        self.gid = gid      
        self.cumret = cumret
        self.holding = holding
        self.type = "Strategy"
        self.cumretGid = None
        self.holdingGid = None




def isGodColumns(col):
    if col.size == 1:
        return col[0].__len__() == 0
    return False

class InputOperation:
    def __init__(self, just_do, left_value, right_value, order_changed):
        self.just_do = just_do
        self.left_value = left_value.input
        self.right_value = right_value.input
        self.order_changed = order_changed


class matrixCommonInfo:
    def __init__(self, rawInput):
        if isinstance(rawInput, gftIO.GftTable):
            rawInput = rawInput.asMatrix()
            self.is_df = True
        elif isinstance(rawInput, pd.DataFrame):
            self.is_df = True
        else:
            self.is_df = False

        if self.is_df:
            self.is_nonsymbol = isGodColumns(rawInput.columns)
            if self.is_nonsymbol:
                rawInput = rawInput[rawInput.columns[0]]
        else:
            self.is_nonsymbol = False
        self.input = rawInput

    def align_matrix(self, common_index, common_columns):
        if self.is_df:
            if common_index is not None:
                self.input = self.input.reindex(common_index)
            if not self.is_nonsymbol and common_columns is not None:
                if common_columns is not None:
                    self.input = self.input[common_columns]

    def get_operation(self, another):
        if self.is_nonsymbol:
            if (another.is_df and not another.is_nonsymbol):
                return InputOperation(False, another, self, True)
        elif self.is_df:
            if another.is_nonsymbol:
                return InputOperation(False, self, another, False)

        return InputOperation(True, self, another, False)

def merge_info_inplace(info_list):
    common_index = None
    common_columns = None
    for info in info_list:
        if info.is_df:
            if common_index is None:
                common_index = info.input.index
            else:
                common_index = np.intersect1d(common_index, info.input.index)
            if not info.is_nonsymbol:
                if common_columns is None:
                    common_columns = info.input.columns
                else:
                    common_columns = np.intersect1d(common_columns, info.input.columns)

    if (common_index is not None) or (common_columns is not None):
        for info in info_list:
            info.align_matrix(common_index, common_columns)

    return info_list


def align_input(*inputs):
    input_list = []
    for input in inputs:
        input_list.append(matrixCommonInfo(input))
    return merge_info_inplace(input_list)



def _findValueColumn(ls_columns):
    raise ValueError("Do not use this def, use find_value_column(data) instead.")

def find_value_column(data):
    for col_name in data.columns:
        if gftIO.get_column_type(data, col_name) == gftIO.PARAMETER_TYPE_NUMBER_NUMRIC:
            return col_name
    raise ValueError("Value Column is not found in {}!".format(data.columns.tolist()))

def find_date_column(data):
    for col_name in data.columns:
        if gftIO.get_column_type(data, col_name) == gftIO.PARAMETER_TYPE_TIMESTAMP:
            return col_name
    raise ValueError("Date Column isnot found in {}!".format(data.columns.tolist()))

class ExtractDictModelData(object):
    """ model data extraction and getting attribute. """
    def __init__(self, model):
        self.model = model

    def get_input_factor(self, oset_idx):
        """ Get oset idx from risk model.
        Keyword Arguments:
        oset_idx: list of oset gid
        """
        if len(oset_idx) < 1:
            return None
        date_index = self.model.get(oset_idx[0], None).asMatrix().index
        ls_factor_b_char = gftIO.strSet2Np(np.array(oset_idx))
        factor_data = pd.Panel({ls_factor_b_char[key]: self.model.get(factor).asMatrix() for key, factor in enumerate(oset_idx)})

        return factor_data.transpose(1, 2, 0)

    def get_output(self, post_fix, oset_idx=None):
        """ get target data from model

        Keyword Arguments:
        oset_idx: list of oset gid
        poset_fix: 'specificRisk', 'ret_cov', '*.ret'
        """
        if oset_idx is None:
            return self.model.get(post_fix, None)
        else:
            factors_output = pd.DataFrame(
                index=self.model[oset_idx[0]+post_fix].index, columns=oset_idx)
            for value in oset_idx:
                factors_output[value] = self.model[value+post_fix]
            factors_output.columns = gftIO.strSet2Np(
                factors_output.columns.values)
            return factors_output



def merge_matrix(old_data, new_data, old_desc, new_desc):
    if new_desc.required_begin_t <= old_desc.required_begin_t:
        return new_data
    if new_desc.required_begin_t <= old_desc.required_end_t:
        # so slice old data
        old_data = old_data[old_data.index < new_desc.required_begin_t]
    #concat old data with new data
    # concat along index, and use outer join for columns.
    return pd.concat(objs=[old_data, new_data],axis=0,join='outer')




def merge_col_tab(old_data, new_data, old_desc, new_desc):
    print ("merge coltabs, size:{0} and {1}".format(str(old_data.shape), str(new_data.shape)))
    if new_desc.required_begin_t <= old_desc.required_begin_t:
        return new_data

    sorted_old_cols = old_data.columns.sort_values()
    sorted_new_cols = new_data.columns.sort_values()
    if not sorted_old_cols.equals(sorted_new_cols):
        raise Exception("New data's columns{0} is not the same as old data's columns{1}".format(str(sorted_new_cols), str(sorted_old_cols)))

    #bcs pt_name may not right from desc
    pt_name = gftIO.get_pt_name(old_data, old_desc.get_pt_name())
    if pt_name is None:
        return new_data

    if new_desc.required_begin_t <= old_desc.required_end_t:
        # so slice old data
        old_data = old_data[old_data[pt_name] < new_desc.required_begin_t]

    # concat old data with new data
    ret = pd.concat(objs=[old_data, new_data],axis=0,join='outer')
    # print("Concated table size:{0}".format(str(ret.shape)))
    return ret


def merge_xarray(old_data, new_data, old_desc, new_desc):
    raise Exception("Not supported yet.")


def merge_data(old_data, new_data, old_desc, new_desc):
    if type(old_data) != type(new_data):
        raise Exception("Can not merge data of differnt types")
    if isinstance(new_data, dict):
        ret = dict()
        for key, val in dict.items():
            old_value = old_data.get(key)
            if old_value is not None:
                ret[key] = merge_data(old_value, val, old_desc, new_desc)
            else:
                ret[key] = val
    if isinstance(new_data, gftIO.GftTable):
        if (new_data.matrix is not None) and (old_data.matrix is not None):
            merged_mtx = merge_matrix(old_data.matrix, new_data.matrix, old_desc, new_desc)
            new_data.matrix = merged_mtx
            new_data.columnTab = None
            return new_data
        if (new_data.columnTab is not None) and (old_data.columnTab is not None):
            merged_col_tab = merge_col_tab(old_data.columnTab, new_data.columnTab, old_desc, new_desc)
            new_data.columnTab = merged_col_tab
            new_data.matrix = None
            return new_data
        raise Exception("Merge GftTable of different type")
    if isinstance(new_data, pd.DataFrame):
        is_new_data_matrix = gftIO.ismatrix(new_data)
        if is_new_data_matrix != gftIO.ismatrix(old_data):
            raise Exception("Merge dataframe of different shape")
        if is_new_data_matrix:
            return merge_matrix(old_data, new_data, old_desc, new_desc)
        else:
            return merge_col_tab(old_data, new_data, old_desc, new_desc)
    if isinstance(new_data, xarray):
        return merge_xarray(old_data, new_data, old_desc, new_desc)
    return new_data



# all caches would be in this struct. so i can get both data and meta.
class CacheData:
    def __init__(self, type, meta, data):
        self.data = data
        self.meta = meta
        self.type = type

    def copy_and_slice_data_with_begin_date(self, begin_date):
        return self

    def copy_and_slice_data_with_end_date(self, end_data):
        return self

    def copy_and_slice_data_with_begin_end_date(self, begin_date, end_date):
        return self


def dumpAll4Cache(type, meta, data, timestamp, filename):
    cache = CacheData(type, meta, data)
    return gftIO.zdump4CacheSever(cache, timestamp, filename)


import pickle
import copy

class Keys:
    def __init__(self):
        pass
    def has_next(self):
        return False
    def next(self):
        return None
    def copy(self):
        return copy.copy(self)

    def reset(self):
        pass
    def size(self):
        return -1

    def key_value(self):
        return None

class Values:
    def __init__(self, values):
        self.values = values
        self.list_size = 1

    def get(self, next_key):
        return None

    def copy(self):
        return copy.copy(self)

    def get_list_size(self):
        return 1


class DataIterator:
    def __init__(self, as_list, is_const, keys: Keys, values: Values):
        self.as_list = as_list
        self.keys = keys
        self.values = values
        self.cur_key = None
        self.list_size = 1
        self.is_const = is_const

    def get_list_size(self):
        if self.as_list:
            return self.values.get_list_size()
        return 1

    def set_as_list(self):
        self.as_list = True
        while self.has_next():
            data = self.next()
            if isinstance(data, list) or isinstance(data, tuple):
                self.list_size = len(data)
                return

    def copy(self):
        return DataIterator(self.as_list, self.is_const, self.keys.copy(), self.values.copy())

    def has_next(self):
        return self.keys.has_next()

    def next(self):
        return self.values.get(self.keys.next())

    def key(self):
        return self.keys.key_value()

    def get_keys(self):
        return self.keys.get_keys()

    def get_columns(self):
        return None

    def get_values(self):
        return self.values

    def reset(self):
        # print("{0} reseted)".format(str(type(self))))
        self.keys.reset()

    def size(self):
        return self.keys.size()

    def __data_desc__(self):
        ret_dict = dict()
        ret_dict['iter_type'] = str(type(self))
        ret_dict['row_size'] = str(self.keys.size())
        ret_dict['col_size'] = str(self.list_size)
        ret_dict['key_type'] = self.keys.key_type()
        ret_dict['val_type'] = self.values.val_type()
        return ret_dict

class IndexKeys(Keys):
    def __init__(self, index):
        self.pos = -1
        self.index = index
        self.last_index = self.index.size - 1

    def has_next(self):
        return self.last_index > self.pos

    def next(self):
        self.pos += 1
        return self.pos

    def key_value(self):
        return self.index[self.pos]

    def reset(self):
        self.pos = -1

    def size(self):
        return self.last_index + 1

    def key_type(self):
        return str(type(self.index))

    def get_keys(self):
        return self.index.values

class IndexValues(Values):
    def __init__(self, source_data):
        self.source_data = source_data
        self.list_size = 1
        if isinstance(source_data, gftIO.GftTable):
            self.matrix = source_data.asMatrix()
        elif isinstance(source_data, pd.DataFrame):
            self.matrix = source_data
        else:
            raise Exception("Not supported type:" + str(type(source_data)))

    def get(self, next_key):
        return self.matrix.iloc[[next_key]].transpose()

    def val_type(self):
        return str(type(self.source_data))



def create_index_iterator(source_data):
    values = IndexValues(source_data)
    keys = IndexKeys(values.matrix.index)
    return DataIterator(False, False, keys, values)


class ColKeys(Keys):
    def __init__(self, columns):
        self.pos = -1
        self.columns = columns
        self.last_index = columns.size

    def has_next(self):
        return self.last_index > self.pos

    def next(self):
        self.pos += 1
        return self.pos

    def key_value(self):
        return self.columns[self.pos]

    def reset(self):
        self.pos = -1

    def size(self):
        return self.last_index + 1

    def key_type(self):
        return str(type(self.columns))

    def get_keys(self):
        return self.columns.values

class ColValues(Values):
    def __init__(self, source_data):
        self.source_data = source_data
        self.list_size = 1
        if isinstance(source_data, gftIO.GftTable):
            self.matrix = source_data.asMatrix()
        elif isinstance(source_data, pd.DataFramea):
            self.matrix = source_data

    def get(self, next_key):
        return self.matrix[[self.matrix.columns[next_key]]]

    def val_type(self):
        return str(type(self.source_data))



def create_column_iterator(source_data):
    values = ColValues(source_data)
    keys = ColKeys(values.matrix.columns)
    return DataIterator(False, False, keys, values)


def int_to_name(name):
    if name == '0' or name == '0.0':
        return 'date'
    if name == '1' or name == '1.0':
        return 'symbol'
    if name == '2' or name == '2.0':
        return 'factor'
    return name

class ItContinue:
    def __init__(self, skip_reason):
        self.reason = skip_reason

class XarrayKeys(Keys):
    def __init__(self, source_data, axis_name='date'):
        if axis_name is None:
            # find axis with timestamp
            self.axis_name = 'date'
        else:
            # confirm axis existed.
            self.axis_name = axis_name
        self.last_index = source_data[self.axis_name].size - 1
        self.pos = -1
        self.axis_idx = source_data[self.axis_name]

    def has_next(self):
        return self.last_index > self.pos

    def next(self):
        self.pos += 1
        return self.axis_idx[self.pos]

    def key_value(self):
        return self.axis_idx[self.pos].values

    def reset(self):
        self.pos = -1

    def size(self):
        return self.last_index + 1

    def key_type(self):
        return str(type(self.axis_idx))

    def get_keys(self):
        return self.axis_idx.values


class XarrayValues(Values):
    def __init__(self, source_data, axis_name='date', index_name='symbol', column_name='factor'):
        self.as_list = False
        if axis_name is None:
            # find axis with timestamp
            self.axis_name = 'date'
        else:
            # confirm axis existed.
            self.axis_name = int_to_name(axis_name)

        if index_name is None:
            self.index_name = 'symbol'
        else:
            self.index_name = int_to_name(index_name)
        if column_name is None:
            self.column_name = 'factor'
        else:
            self.column_name = int_to_name(column_name)
        self.source_data = source_data.transpose(self.axis_name, self.index_name, self.column_name)
        self.list_size = 1

    def get(self, next_key):
        return self.source_data.loc[next_key,:,:].to_pandas()

    def val_type(self):
        return str(type(self.source_data))


def create_xarray_iterator(source_data, axis_name = 'date', index_name = 'symbol', column_name = 'factor'):
    values = XarrayValues(source_data, axis_name, index_name, column_name)
    keys = XarrayKeys(source_data, values.axis_name)
    return DataIterator(False, False, keys, values)





class DictKeys(Keys):
    def __init__(self, dic_data):
        self.it = dic_data.items().__iter__()
        self.count = dic_data.__len__()
        self._key = None
        self.source_data = dic_data


    def has_next(self):
        return self.count > 0

    def next(self):
        self.count -= 1
        key_value = self.it.__next__()
        self._key = key_value[0]
        return key_value[1]

    def copy(self):
        return DictKeys(self.source_data)

    def reset(self):
        self.count = self.source_data.__len__()
        self.it = self.source_data.items().__iter__()

    def size(self):
        return self.source_data.__len__()

    def key_value(self):
        return self._key

    def get_keys(self):
        return self.source_data.keys()

    def key_type(self):
        return str(type(self.source_data))


class DictValues(Values):
    def __init__(self, dic_data: dict):
        self.source_data = dic_data
        self.list_size = 1
        for key, value in dic_data.items():
            if isinstance(value, list) or isinstance(value, tuple):
                self.list_size = len(value)
                return

    def get(self, next_key):
        return next_key

    def val_type(self):
        return str(type(self.source_data))


def create_dict_iterator(dic_data):
    values = DictValues(dic_data)
    keys = DictKeys(dic_data)
    return DataIterator(False, False, keys, values)


def prepare_iterator(*iterators):
    available_it = None
    const_iterators = list()
    ret_list = list()

    for it in iterators:
        if isinstance(it, DataIterator):
            it_copy = it.copy()
        else:
            it_copy = create_const_copy_iterator(it, None)
        if it_copy.is_const:
            const_iterators.append(it_copy)
        else:
            available_it = it_copy
        ret_list.append(it_copy)

    if available_it is None:
        return None
    for const_it in const_iterators:
        const_it.keys.reset_other_keys(available_it.keys)
    return ret_list

class ListValues(Values):
    def __init__(self, *iterators):
        self.iter_list = list()
        for it in iterators:
            if isinstance(it.values, ListValues):
                for it in it.values.iter_list:
                    self.iter_list.append(it.copy())
            else:
                self.iter_list.append(it.copy())
        self.data_list = list()
        self.list_range = range(len(iterators))
        total_size = 0
        for it in self.iter_list:
            total_size += it.get_list_size()
        self.list_size = total_size

    def get_underlaying_it(self, index):
        for it in self.iter_list:
            it_list_size = it.get_list_size()
            if it_list_size > index:
                if isinstance(it.values, ListValues):
                    return it.values.get_underlaying_it(index)
                return index, it
            else:
                index -= it_list_size
        return index, None

    def copy(self):
        return ListValues(*self.iter_list)

    def reset(self):
        # print("ListValue reseted")
        for it in self.iter_list:
            it.reset()


    def get(self, next_key):
        self.data_list.clear()
        skip_row = None
        for it in self.iter_list:
            val = it.next()
            if isinstance(val, ItContinue):
                skip_row = val
                continue
            if it.as_list:
                self.data_list.extend(val)
            else:
                self.data_list.append(val)
        if skip_row is not None:
            return skip_row
        return self.data_list

    def val_type(self):
        return str(type(self.iter_list))


class ReferenceKeys(Keys):
    def __init__(self, first_availkeys):
        if isinstance(first_availkeys, ReferenceKeys):
            first_availkeys = first_availkeys.keys
        self.keys = first_availkeys.copy()

    def has_next(self):
        return self.keys.has_next()


    def next(self):
        return self.keys.next()


    def copy(self):
        return ReferenceKeys(self.keys.copy())

    def reset(self):
        self.keys.reset()


    def size(self):
        return self.keys.size()

    def key_value(self):
        return self.keys.key_value()

    def key_type(self):
        return self.keys.key_type()

    def get_keys(self):
        return self.keys.get_keys()

class ExtractValues(Values):
    def __init__(self, iter: DataIterator, index):
        index = int(index)
        if iter.list_size < index:
            raise Exception("list({0}) not long enough, required{1}".format(str(iter.list_size), str(index)))
        if isinstance(iter, ListIterator):
            index, iter = iter.values.get_underlaying_it(index)
        self.iter = iter.copy()
        self.values = iter.values
        self.index = index
        self.list_size = self.iter.list_size

    def get(self, next_key):
        if self.iter.as_list:
            val = self.values.get(next_key)
            if isinstance(val, ItContinue):
                return val
            return val[self.index]
        else:
            return self.values.get(next_key)

    def val_type(self):
        return self.values.val_type()


def get_property(node, pro_name):
    for entry in node.node_prop.props.entries:
        if (entry.key == pro_name):
            return entry.value
    return None


class ExtractListValues(Values):
    def __init__(self, iter: DataIterator, indexes: str):
        splited = indexes.split(',')
        int_indexes = list()
        for idx in splited:
            int_indexes.append(int(idx))
        if isinstance(iter.values, ExtractListValues):
            sub_idx = list()
            for i in int_indexes:
                sub_idx.append(iter.values.int_indexes[i])
            int_indexes = sub_idx
            iter = iter.values.source_data
        self.iter = iter
        self.values = iter.values
        self.int_indexes = int_indexes
        self.data_list = list()

    def get(self, next_key):
        self.data_list.clear()
        vals = self.values.get(next_key)
        if isinstance(vals, ItContinue):
            return vals
        for i in self.int_indexes:
            self.data_list.append(vals[i])
        return self.data_list


def create_extract_values(it, index):
    values = ExtractValues(it, index)
    if values.index == 0 and values.iter.as_list == False:
        return values.iter.copy()
    keys = ReferenceKeys(values.iter.keys)
    return DataIterator(False, False, keys, values)

def create_extract_multi_values(it, indexes_str):
    values = ExtractListValues(it, indexes_str)
    keys = ReferenceKeys(values.iter.keys)
    return DataIterator(True, False, keys, values)


class ListIterator(DataIterator):
    def __init__(self, keys, values: ListValues):
        DataIterator.__init__(self, True, False, keys, values)

    def reset(self):
        # print("ListIterator reseted.")
        self.keys.reset()
        self.values.reset()

def create_list_iterator(*iterators):
    keys = ReferenceKeys(iterators[0].keys)
    values = ListValues(*iterators)
    return ListIterator(keys, values)

class ConstIteratorKeys(Keys):
    def __init__(self, other_keys):
        if other_keys is not None:
            other_keys = other_keys.copy()
        self.other_keys = other_keys

    def reset_other_keys(self, other_key):
        self.other_keys = other_key.copy()


    def has_next(self):
        return self.other_keys.has_next()

    def next(self):
        return self.other_keys.next()


    def copy(self):
        return ConstIteratorKeys(self.other_keys)

    def reset(self):
        self.other_keys.reset()

    def size(self):
        return self.other_keys.size()

    def key_value(self):
        return self.other_keys.key_value()

    def key_type(self):
        return self.other_keys.key_type()

class ConstIteratorValues(Values):
    def __init__(self, const_val):
        self.const_val = const_val

    def get(self, next_key):
        return self.const_val

    def val_type(self):
        return type(str(self.const_val))

def create_const_iterator(const_val, othter_keys):
    keys = ConstIteratorKeys(othter_keys)
    values = ConstIteratorValues(const_val)
    return DataIterator(False, True, keys, values)

class ConstCopyIteratorValues(ConstIteratorValues):
    def __init__(self, const_val):
        self.const_val = const_val
    def get(self, next_key):
        return copy.deepcopy(self.const_val)

def create_const_copy_iterator(const_val, other_iterator_keys):
    keys = ConstIteratorKeys(other_iterator_keys)
    values = ConstCopyIteratorValues(const_val)
    return DataIterator(False, True, keys, values)


def getCacheData(value):
    cache = pickle.loads(value)
    if isinstance(cache, CacheData):
        return cache.type, cache.meta, cache.data
    raise Exception("Cache type is not gsMeta.CacheData")


def slice_redundant_result_and_wrap_gft_table_is_necessary(obj, meta):
    if (meta.required_begin_t > meta.input_begin_t) or (meta.required_end_t < meta.input_end_t):
        # may have redundant date in result.
        # print("Slice redundant data in result.")
        obj = gftIO.slice_data_inplace_and_ret(obj, gftIO.get_pt_name(obj, meta.get_pt_name()), meta.required_begin_t, meta.required_end_t)

    return gftIO.wrap_gfttable_dataframe_clean_gid(obj)

import xarray as xr

def create_xarray_from_dic(data_dict, date_name = 'date', symbol_name='symbol', factor_name='factor'):
    variables = dict()
    for key, value in data_dict.items():
        if isinstance(value, gftIO.GftTable):
            variables[key] = xr.DataArray(value.asMatrix(), dims=[date_name, symbol_name])
        elif isinstance(value, pd.DataFrame):
            variables[key] = xr.DataArray(value, dims=[date_name, symbol_name])
        else:
            raise Exception("Value[{0}] of type:{1} is not acceptable".format(str(key), str(type(value))))

    combined = xr.Dataset(variables).to_array(dim=factor_name)
    return combined

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


def get_property_in_nodeinfo(node_info, key_name):
    for entry in node_info.node_prop.props.entries:
        if entry.key == key_name:
            return entry.value
    return None


def crypt(PlainBytes, KeyBytes):
    keystreamList = []
    cipherList = []

    keyLen = len(KeyBytes)
    plainLen = len(PlainBytes)
    S = bytearray(256)
    for i in range(256):
        S[i] = i


    j = 0
    for i in range(256):
        j = (j + S[i] + KeyBytes[i % keyLen]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    for m in range(plainLen):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        keystreamList.append(k)
        cipherList.append(k ^ PlainBytes[m])

    ret = bytearray(len(cipherList))
    for i in range(len(cipherList)):
        ret[i] = cipherList[i]
    return bytes(ret)

freq_gids = ["DAILY", "BUSINESSDAILY_SH_STK", "WEEKDAY", "WEEKLYFIRST", "WEEKLYMIDDLE", "WEEKLYLAST",
                 "MONTHLYFIRST", "MONTHLYMIDDLE", "MONTHLYLAST", "QUARTERLYFIRST", "QUARTERLYMIDDLE", "QUARTERLYLAST",
                 "SEMIANNUALFIRST", "SEMIANNUALMIDDLE", "SEMIANNUALLAST", "YEARLYFIRST", "YEARLYMIDDLE", "YEARLYLAST"]

freq_gid_set = set(freq_gids)
freq_gid_set.add("GFT")


def is_gs_gid(txt:str):
    if (txt.__len__() == 32):
        for c in txt:
            if (c < '0' and c >'F') or (c > '9' and c < 'A'):
                return False
        return True
    else:
        return freq_gid_set.__contains__(txt)

from datetime import datetime
from datetime import timezone

local_tz = datetime.now(timezone.utc).astimezone().tzinfo

def str2datetime(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

def find_prop(prop_container, key, def_val = None):
    for entry in prop_container.props.entries:
        if entry.key == key:
            return entry.value
    return def_val