# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gftIO


def CalculateReturn(context,input):
    if isinstance(input, gftIO.GftTable):
        input = input.asMatrix()
    return input.pct_change().dropna()
