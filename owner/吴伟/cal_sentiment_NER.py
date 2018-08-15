# <codecell>

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from requests.exceptions import ConnectionError, ChunkedEncodingError
from snownlp import SnowNLP
import logging
from pyltp import SentenceSplitter
import os
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import itertools
import matplotlib.pyplot as plt
import datetime
from lib.gftTools.word2Vec import preprocessing
from collections import defaultdict

LTP_DATA_DIR = '/mnt/hdfs/cacheServer/aiData/pyltp/'  # ltp模型目录的路径

def cal_sentiment_NER(df_text):
    """
    natural language processing on every row from the input.
    1. for loop dataframe:
    2. preprocess text in the df.
    3. get entity using pyLTP
    4. get sentiment, keywords, summary using SnowNLP.
    5. append result to df
    Keyword Arguments:
    df_text --
    """
    # 词性标注
    pos_model_path = os.path.join(LTP_DATA_DIR,
                                  'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型

    # 命名实体识别
    ner_model_path = os.path.join(LTP_DATA_DIR,
                                  'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`

    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型

    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    
    if isinstance(df_text, gftIO.GftTable):
        df_text = df_text.as_mutable_column_tab()
    df_result = pd.DataFrame(columns=[
        'datetime', 'people', 'geography', 'organization', 'keyword', 'summary',
        'score'
    ])
    for item in df_text[:10].iterrows():
        #  print(item[1]['Conclusion'])
        logging.info(item[0])

        text = item[1]['Conclusion']
        datetime = item[1]['WritingDate']
        if not pd.isnull(text):
            text_split = preprocessing.preprocess_string(text)
            # 词性标注
            #            postagger = Postagger()  # 初始化实例

            words = text_split.split()  # 分词结果
            postags = postagger.postag(words)  # 词性标注
            netags = recognizer.recognize(words, postags)  # 命名实体识别

            dict_netags = defaultdict(list)
            ls_netags = list(zip(netags, words))
            for x, y in ls_netags:
                dict_netags[x].append(y)

            s = SnowNLP(text)
            score = s.sentiments * 2
            # # 人名（Nh）、地名（Ns）、机构名（Ni。）
            # # B、I、E、S
            ls_organization = [
                dict_netags[x] for x in ['S-Ni', 'B-Ni', 'E-Ni', 'I-Ni']
            ]
            ls_people = [
                dict_netags[x] for x in ['S-Nh', 'B-Nh', 'E-Nh', 'I-Nh']
            ]
            ls_geography = [
                dict_netags[x] for x in ['S-Ns', 'B-Ns', 'E-Ns', 'I-Ns']
            ]
            try:
                df_result = df_result.append(
                    {
                        'datetime':
                        datetime,
                        'keyword':
                        ','.join(s.keywords()),
                        'organization':
                        list(itertools.chain.from_iterable(ls_organization)),
                        'people':
                        list(itertools.chain.from_iterable(ls_people)),
                        'geography':
                        list(itertools.chain.from_iterable(ls_geography)),
                        'summary':
                        ';'.join(s.summary()),
                        'score':
                        score
                        # 'text': text,
                    },
                    ignore_index=True)
            except:
                continue
    return df_result


# <codecell>

import os

env_dist = os.environ # environ是在os.py中定义的一个dict environ = {}

print(env_dist.get('HDFS_ROOT'))


# <codecell>

