# <codecell>

# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import pandas as pd
import logging
import os


engine = create_engine(
    'mysql+mysqlconnector://datatec:0.618@[172.16.103.103]:3306/JYDB',
    echo=False)


def read_mysql_database(sql_statement):
    """ retrieve articles from mysql database
    Keyword Arguments:
    sql_statement          -- 

    Return:
    dataframe
    """
    df_table = pd.read_sql(sql_statement, engine)
    return df_table


# <codecell>

