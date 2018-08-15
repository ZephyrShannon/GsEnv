# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
from sklearn.svm import SVC

def CreateSVMClassifier(context, dict_parm):
    clf = SVC(C  =  gsUtils.getParm(dict_parm, 'C', 1.0),
            kernel  = gsUtils.getParm(dict_parm, 'kernel', 'rbf'),
            degree = gsUtils.getParm(dict_parm, 'degree', 3),
            gamma  = gsUtils.getParm(dict_parm, 'gamma', 'auto'),
            coef0 =gsUtils.getParm(dict_parm, 'coef0 ', 0) ,
            probability = gsUtils.getParm(dict_parm, 'probability ', False),
            shrinking  = gsUtils.getParm(dict_parm, 'shrinking',True),
            tol = gsUtils.getParm(dict_parm, 'tol', 0.001) ,
            cache_size =gsUtils.getParm(dict_parm, 'cache_size ', 200),
            class_weight = gsUtils.getParm(dict_parm, 'class_weight', None),
            verbose = gsUtils.getParm(dict_parm, 'verbose', False),
            max_iter = gsUtils.getParm(dict_parm, 'n_jobs', -1),
            decision_function_shape=gsUtils.getParm(dict_parm,'decision_function_shape', 'ovr'),
            random_state = gsUtils.getParm(dict_parm, 'random_state', None)
            )
                          
    return clf

# <codecell>


