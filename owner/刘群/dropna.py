# <codecell>




def dropna(data ,non_na_pct):
    df = data.asMatrix()
    
    # count required number of non_na cross-sectionally (axis=0)
    non_na_amount = int(df.shape[0]*non_na_pct)
    df_dropna_1 = df.dropna(thresh=non_na_amount, axis=1)

    # dropna if it is empty column (axis=1)
    df_dropna_2 = df_dropna_1.dropna(axis=1, how='all')
    
    return df_dropna_2


# <codecell>

