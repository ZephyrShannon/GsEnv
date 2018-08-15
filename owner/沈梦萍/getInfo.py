# <codecell>

import numpy as np
import pandas as pd


def getInfo(context,data):
    df = data.asColumnTab().copy()
    column_type= gftIO.get_columns_type_dict(df)
    o_count = 0
    v_count = 0
    t_count = 0
    result = {}
    result['rows_count'] = df.shape[0]  
    df.dropna(inplace=True)
    for key in column_type:
            if column_type[key] == gftIO.PARAMETER_TYPE_TIMESTAMP:
                result['t_count'] = result.get('t_count',0)+1
                result['unique_t_count'] = result.get('unique_t_count',0)+len(df[key].unique())
                result['max_t'] = result.get('max_t',max(df[key]))
                result['min_t'] = result.get('min_t',min(df[key]))
            elif column_type[key]== gftIO.PARAMETER_TYPE_UUID:
                result['o_count'] = result.get('o_count',0)+1
                result['unique_o_count'] = result.get('unique_o_count',0)+len(df[key].unique())
            elif column_type[key]== gftIO.PARAMETER_TYPE_NUMBER_NUMRIC:
                result['v_count'] = result.get('v_count',0)+1
                result['max_v'] = result.get('max_v',0)+max(df[key])
                result['min_v'] = result.get('min_v',0)+min(df[key])
                result['non_zero_value_count'] = result.get('non_zero_value_count',df[key][df[key]!=0].count())
                result['avg_v'] = result.get('avg_v',df[key].mean())
                result['std_v'] = result.get('std_v',df[key].std())
                result['med_v'] = result.get('std_v',df[key].median())
                #test if v_all_integer
                v_integer = 0
                for i in np.nan_to_num(df[key].values):
                    if int(i)!=i:
                        v_integer += 1
                if v_integer != 0:
                    result['v_all_integer'] =0
                else:
                    result['v_all_integer'] = 1
    #reset unique counts if count>1            
    if 'o_count' in result.keys() and result['o_count']>1:
        result.pop('unique_o_count')
    if 't_count' in result.keys() and result['t_count']>1:
        result.pop('unique_t_count')
        result.pop('max_t')
        result.pop('min_t')
    if 'v_count' in result.keys() and result['v_count']>1:
        result.pop('max_v')
        result.pop('min_v')
        result.pop('non_zero_value_count')
        result.pop('avg_v')
        result.pop('std_v')
        result.pop('med_v')
        result.pop('v_all_integer')
    #set o_count if o column not exists
    if 'o_count' not in result.keys():
        result['o_count'] = 0
    #find v_fullness
    if result['o_count']==1 and result['t_count']==1 and result['v_count']==1:
        df_mt = data.asMatrix()
        v_fullness = sum(df_mt.count())/df_mt.size
        result['v_fullness'] = v_fullness
    #get t_timedelta
    if 't_count' in result.keys():
        result['t_timedelta'] = ((result['max_t']-result['min_t'])/ result['unique_t_count']).days
    #calculate tbl_cnt
    if isinstance(df, dict) is True:
        result['tbl_cnt'] = len(tbl_cnt.keys())
    else:
        result['tbl_cnt'] = 0
    return result

# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return getInfo

def create_func_obj(data):
    return gftIO.GsFuncObj('6A875CE2B92D445C99BDA29F79FC0938', '3D275B65412E42A5933AC376213609C0', getInfo,  False, data)
# end 

# ##END CODES FOR CREATE_LAMBDA##
