# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
from sklearn.neighbors import KNeighborsClassifier


def CreateKNNClassifier(context,dict_parm):
    clf = KNeighborsClassifier(n_neighbors  =  gsUtils.getParm(dict_parm, 'n_neighbors', 5),
            weights  = gsUtils.getParm(dict_parm, 'weights', 'uniform'),
            algorithm = gsUtils.getParm(dict_parm, 'algorithm', 'auto'),
            leaf_size  = gsUtils.getParm(dict_parm, 'leaf_size', 30),
            p =gsUtils.getParm(dict_parm, 'p ', 2) ,
            metric = gsUtils.getParm(dict_parm, 'metric ', 'minkowski'),
            n_jobs  = gsUtils.getParm(dict_parm, 'shrinking',1),
            )               
    return clf
