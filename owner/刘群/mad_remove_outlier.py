# <codecell>

# need to apply xarray to avoid loop
import pandas as pd 
import numpy as np

def mad_remove_outlier(factor_dic):

    factor_ls = list(factor_dic.keys())
    
    date_ls = list(factor_dic[factor_ls[0]].index)

    x_dic={}
    
    for date in date_ls:
        
        df_date = pd.DataFrame()
        
        for factor in factor_ls:
            
            df_factor = factor_dic[factor].T.rename(columns={date:factor})            
            
            series = df_factor[factor]
            
            mad = series.mad()
            median = series.median()
            max = median + 3 * 1.4826 * mad
            min = median - 3 * 1.4826 * mad
            
            # to get back original nans
            
            df = series.to_frame()
            df['na'] = df[factor].isnull()
                        
            df[factor].where(df[factor]<max, max, inplace = True)
            df[factor].where(df[factor]>min, min, inplace = True)
            
            df.loc[df.na == True, factor] = np.nan
            
            df_date = pd.concat([df_date, df[factor]],axis=1)

            
        x_dic[date] = df_date

    return x_dic


# <codecell>

