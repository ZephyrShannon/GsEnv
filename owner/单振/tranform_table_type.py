# <codecell>




def tranform_table_type(orig_df ,matrix_or_columntab):
    """
    transform dataframe type:
    column table -> matrix 
    or
    matrix -> column table
     Parameters
    ----------
    orig_df: input a dataframe of gftIO.GftTable
    matrix_or_columntab: [0 ,1]
                         0: column table -> matrix, if the input dataframe is a matrix, just return it.
                         1: matrix -> column table 
                         
    """
    if isinstance(orig_df, gftIO.GftTable):
        if matrix_or_columntab == 0:
            return orig_df.as_mutable_matrix()
        else:
            return orig_df.as_mutable_column_tab()
    elif isinstance(orig_df, pd.DataFrame):
        if gftIO.ismatrix(orig_df):
            if matrix_or_columntab == 0:
                return orig_df
            else:
                return gftIO.convertMatrix2ColumnTab(orig_df.copy())
        else:
            if matrix_or_columntab == 0:
                return gftIO.convertColumnTabl2Matrix(orig_df.copy())
            else:
                return orig_df
                
            


# <codecell>

