# <codecell>

# -*- coding: utf-8 -*-
import pandas as pd
import hashlib
from urllib.parse import quote_plus, urlparse, parse_qs


def hash(characters):
    pk_str = 'https://www.google.com.hk/search?hl=en&source=hp&q='+quote_plus(characters)
    pk_md5 = hashlib.md5(pk_str.encode('utf-8')).hexdigest().upper()
    return hashlib.md5(pk_md5.encode('utf-8')).hexdigest().upper()

def similar_words(model ,key_words ,topn):
    """
    return most topn similar words in the model
    
    Parameter:
    model: word2vec model trained via gensim
    key_words: input key words
    topn: return n most similar words
    """
    sim_words = model.most_similar(key_words,topn=topn)
    df = pd.DataFrame(sim_words, columns=['word','similarity'])
    df['word'] = df['word'].apply(hash)
    #df=pd.DataFrame([('以张',0.1),('竹宫',0.1)], columns=['word','similarity'])
    #df['word'] = df['word'].apply(hash)
    df['word'] = gftIO.gidStrArray2CharArray(df['word'].values.copy())
    return df

# <codecell>

