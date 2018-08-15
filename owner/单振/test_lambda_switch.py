# <codecell>

import numpy as np
import pandas as pd

# <codecell>

def test_lambda_switch(context, data, choice, operators):
    if choice > len(operators) or choice <= 0:
        raise Exception("Incorrect choice[{0}]".format(str(choice)))
    return operators[choice - 1](j=data)

# <codecell>

