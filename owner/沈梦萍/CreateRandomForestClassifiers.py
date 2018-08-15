# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
from sklearn.ensemble import RandomForestClassifier

def CreateRandomForestClassifiers(context,dict_parm):
    clf = RandomForestClassifier(n_estimators =  gsUtils.getParm(dict_parm, 'n_estimators', 10),
                                criterion = gsUtils.getParm(dict_parm, 'criterion', 'gini'),
                                max_depth = gsUtils.getParm(dict_parm, 'max_depth', None),
                                min_samples_split = gsUtils.getParm(dict_parm, 'min_samples_split', 2),
                                min_samples_leaf=gsUtils.getParm(dict_parm, 'min_samples_leaf', 1) ,
                                min_weight_fraction_leaf = gsUtils.getParm(dict_parm, 'min_weight_fraction_leaf', 0.0),
                                max_features = gsUtils.getParm(dict_parm, 'max_features', 'auto'),
                                max_leaf_nodes = gsUtils.getParm(dict_parm, 'max_leaf_nodes', None) ,
                                min_impurity_split=gsUtils.getParm(dict_parm, 'min_impurity_split', 1e-07),
                                bootstrap = gsUtils.getParm(dict_parm, 'bootstrap', True),
                                oob_score = gsUtils.getParm(dict_parm, 'oob_score', False),
                                n_jobs = gsUtils.getParm(dict_parm, 'n_jobs', 1),
                                random_state=gsUtils.getParm(dict_parm, 'random_state', None),
                                verbose= gsUtils.getParm(dict_parm, 'verbose', 0),
                                warm_start = gsUtils.getParm(dict_parm, 'warm_start', False),
                                class_weight=gsUtils.getParm(dict_parm, 'class_weight', None)
                                  )
                          
    return clf
