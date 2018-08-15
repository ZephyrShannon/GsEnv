# <codecell>

import numpy as np
import pandas as pd


# <codecell>




# <codecell>

def transform_to_readable(context,data,oper):
    if oper == 1:
        if isinstance(data, gftIO.GftTable):
            if data.matrix is not None:
                return data.matrix.reset_index()
    else:
        raise Exception("Operation[{0}] is not implemented".format(str(oper)))


	

# <codecell>

