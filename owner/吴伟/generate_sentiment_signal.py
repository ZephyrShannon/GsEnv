# <codecell>

import pandas as pd


def generate_sentiment_signal(df_nlp):
    df_nlp = df_nlp.as_mutable_column_tab()
    df_sentiment = df_nlp[['datetime', 'score']].groupby('datetime').mean()
    df_sentiment['text_count'] = df_nlp[['datetime',
                                         'score']].groupby('datetime').count().astype(float)
    return df_sentiment.reset_index()

# <codecell>

