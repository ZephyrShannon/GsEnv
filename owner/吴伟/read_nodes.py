# <codecell>

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch skill gid and extract page.
preprocess text, remove punctuation, remove stopwords, tokenize.
train word2vec model.
save model.
"""
import gensim
import logging
import multiprocessing
import os
import sys
from time import time
from gensim.models.word2vec import LineSentence
# from ylib import ylog
from lib.gftTools import gftIO
from lib.gftTools.word2Vec import preprocessing
import pandas as pd
import numpy as np
# test fetch graph
prod_url = 'http://172.16.103.106:9080'
test_user_name = 'wuwei'
test_pwd = 'gft'
gs_call = gftIO.GSCall(prod_url, test_user_name, test_pwd)


def complete_dir_path(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not dir_path.endswith('/'):
        return dir_path + '/'
    else:
        return dir_path


def read_nodes(ls_gid):
    df_nodes = pd.DataFrame(columns=['WritingDate','Conclusion'])
    logging.info("extract pages")
    for page_id in ls_gid:
        logging.info(page_id)
        try:
            text = gs_call.get_nodes_binary_data([page_id])
        except DecodeError:
            continue
        page = text.entries[0].data.data.decode('utf-8')
        df_nodes = df_nodes.append(pd.DataFrame(data={'WritingDate':[np.datetime64('today')],'Conclusion':[page]}),ignore_index=True)
        logging.debug(text)
    return df_nodes


# <codecell>

