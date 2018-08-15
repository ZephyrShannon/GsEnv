# <codecell>

# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import pandas as pd
import logging
import os


engine = create_engine(
    'mysql+mysqlconnector://datatec:0.618@[172.16.103.103]:3306/JYDB',
    echo=False)

def retrieve_data_from_MySQL(date ,RMDB_table):
    """ retrieve articles from mysql database
    Keyword Arguments:
    date          -- timestamp
    RMDB_table    -- JYDB table name

    Return:
    dataframe
    """
    df_table = pd.DataFrame()
    for dt in date[-3:]:
        sql_syntax = '''SELECT * FROM %s where WritingDate = "%s" limit 99999;''' % (
            RMDB_table, dt.date().strftime("%Y-%m-%d"))
        df_table = df_table.append(pd.read_sql(sql_syntax, engine))
    return df_table


# <markdowncell>

# !pip install mysql-connector-python-rf tqdm

# <codecell>

