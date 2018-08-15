# <codecell>

import numpy as np
import pandas as pd

def ReplaceGid(x,y):
    raise Exception("To be implemented")

# <codecell>

from lib.gftTools import gftIO
x0 = gftIO.zload("/home/jovyan/.gft/data/x0.pkl")
x1 = gftIO.zload("/home/jovyan/.gft/data/x1.pkl")

# <codecell>

x0

# <codecell>

type(x1)

# <codecell>

len(x1)

# <codecell>

dict_data = x0

# <codecell>

type(dict_data)

# <codecell>

dict_data[2]

# <codecell>

ls_data = [i.asColumnTab() for i in dict_data]

# <codecell>

ls_data[3].shape

# <codecell>

dict_data_new=x1

# <codecell>

len(dict_data_new)

# <codecell>

dict_data_new[5]

# <codecell>

dict_data[3].asColumnTab()

# <codecell>

dict_data_new.keys()

# <codecell>

dict_data[5].gid

# <codecell>



# <codecell>



# <codecell>

ls_data = [i.gid for i in dict_data]

# <codecell>

ls_gidname = [i.gid for i in dict_data]

# <codecell>

ls_gidname

# <codecell>

dict_data[4]

# <codecell>



# <codecell>

dict_data_new[4]

# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>


