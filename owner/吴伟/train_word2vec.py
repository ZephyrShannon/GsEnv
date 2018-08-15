# <codecell>


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
# from preprocessing import complete_dir_path

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

    
def extract_pages(ls_pageid, gs_call):
    """ Extract nodes read only documents from input list of gid,
    preprocess text, remove punctuation, remove stopwords, tokenize.
    """
    from tempfile import gettempdir
    tmp_dir = gettempdir()
    output = open(tmp_dir + '/test.txt', 'wb')
    logging.info("extract pages")
    for page_id in ls_pageid:
        logging.info(page_id)
        try:
            text = gs_call.get_nodes_binary_data([page_id])
        except DecodeError:
            continue
        page = text.entries[0].data.data.decode('utf-8')
        text = preprocessing.preprocess_string(page)
        # ylog.debug(text)
        output.write(text.encode('utf-8') + '\n'.encode('utf-8'))
    output.close()

    
def train_word2vec(ls_gid):
    """
    extract page from gid, preprocessing text and train.
    
    Return:
    word2vec model
    """
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info("start training")
    extract_pages(ls_gid, gs_call)
    from tempfile import gettempdir
    tmp_dir = gettempdir()
    txt_path = tmp_dir + '/test.txt'
    model = gensim.models.Word2Vec(
        LineSentence(txt_path),
        size=200,
        window=5,
        min_count=2,
        workers=multiprocessing.cpu_count())
    return model.wv
    

# <codecell>

