# <codecell>

import pandas as pd


def resample(data_dic, frequency):
      
    dic = {}
    
    # transfer to dataframe
    
    for key, value in data_dic.items():
        if isinstance(value, gftIO.GftTable):
            df = value.asMatrix()
            if sum(df.count()) == df.shape[1]:
                df = value.asColumnTab().dropna()            
        elif isinstance(value, pd.DataFrame):
            df = value
        else:
            raise Exception("Can not resample data of type:" + str(type(data)))
                
        df_freq = sort_freq(df,frequency)
        
        dic[key]=df_freq

    return dic
        


# <codecell>

def sort_freq(df,frequency):

    df.sort_index(inplace = True)
    
    # sort by frequency
    if frequency == 'monthly':
        df_freq = df.asfreq('BM',method = 'ffill') # last working day of the month, fill na with last observation
    elif frequency == 'weekly':
        df_freq = df.resample('W-FRI').last() # last working day of the week, fill na with last observation
    elif frequency == 'daily':
        bdays = pd.bdate_range(test.index[0],test.index[-1])
        df_freq = df.reindex(bdays, method = 'ffill') # daily data, ffill
    else:
        raise Exception('The frequency can only be "monthly", "weekly" or"daily"')
    return df_freq

# <codecell>

