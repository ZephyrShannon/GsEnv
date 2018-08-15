# <codecell>

import numpy as np
import pandas as pd


def log_ret(rets):
    """Log of return relatives, ln(1+r), for a given DataFrame rets."""
    return np.log(rets + 1)


def calculate_rolling_mean(context,input_data,window):
    """ calculate rolling mean of a dataframe
    """
    if isinstance(input_data, gftIO.GftTable):
        input_data = input_data.asMatrix().copy()
        input_data = log_ret(input_data)
        
    return input_data.rolling(window=window).mean()
