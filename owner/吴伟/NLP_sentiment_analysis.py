# <codecell>

from snownlp import SnowNLP
import pandas as pd
from tqdm import tqdm


def NLP_sentiment_analysis(df_text):
    """
    natural language processing sentiment analysis on every row from the input.
    1. for loop dataframe:
    2. preprocess text in the df.
    3. get sentiment using SnowNLP.
    4. append result to df
    Keyword Arguments:
    df_text --  mysql table dataframe
    """
    df_text = df_text.as_mutable_column_tab()
    df_sentiment = pd.DataFrame()
    for item in df_text.iterrows():
        text = item[1]['Conclusion']
        datetime = item[1]['WritingDate']
        if text:
            try:
                s = SnowNLP(text)
                score = s.sentiments * 2
                df_sentiment = df_sentiment.append(
                    {
                        'datetime': datetime,
                        'score': score
                    },
                    ignore_index=True)
            except:
                continue
    return df_sentiment

# <codecell>

