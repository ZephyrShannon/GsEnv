# <codecell>

# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import pandas as pd
import logging
import os


engine = create_engine(
    'mysql+mysqlconnector://datatec:0.618@[172.16.103.103]:3306/JYDB',
    echo=False)



def read_RMDB_table(db_name ,table_name ,tbl_columns ,t_filter_col_name ,t_values):
    """ retrieve articles from mysql database
    Keyword Arguments:
    date          -- timestamp
    RMDB_table    -- JYDB table name

    Return:
    dataframe
    """
    date = [x.date().strftime("%Y-%m-%d") for x in t_values[-400:]]
    sql_syntax = '''SELECT %s FROM %s.%s where %s in %s limit 99999999999;'''%(tbl_columns, db_name, table_name, t_filter_col_name, str(tuple(date)))
    df_table = pd.read_sql(sql_syntax, engine)
    return df_table


# <codecell>

