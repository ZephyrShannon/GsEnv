# <codecell>

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from lib.gftTools import gsUtils


def CreateDecisionTreeClassifer(dict_parm):
    clf = DecisionTreeClassifier(criterion =  gsUtils.getParm(dict_parm, 'criterion', 'gini'),
                                splitter = gsUtils.getParm(dict_parm, 'splitter', 'best'),
                                max_depth = gsUtils.getParm(dict_parm, 'max_depth', None),
                                min_samples_split = gsUtils.getParm(dict_parm, 'min_samples_split', 2),
                                min_samples_leaf=gsUtils.getParm(dict_parm, 'min_samples_leaf', 1) ,
                                min_weight_fraction_leaf = gsUtils.getParm(dict_parm, 'min_weight_fraction_leaf', 0.0),
                                max_features = gsUtils.getParm(dict_parm, 'max_features', None),
                                random_state = gsUtils.getParm(dict_parm, 'random_state', None),
                                max_leaf_nodes = gsUtils.getParm(dict_parm, 'max_leaf_nodes', None) ,
                                min_impurity_decrease=gsUtils.getParm(dict_parm, 'min_impurity_decrease', 0.0),
                                min_impurity_split = gsUtils.getParm(dict_parm, 'min_impurity_split', None),
                                class_weight = gsUtils.getParm(dict_parm, 'class_weight', None),
                                presort = gsUtils.getParm(dict_parm, 'presort', False)
                                  )
    return clf

# <codecell>

dict_parm = {}
CreateDecisionTreeClassifer(dict_parm)
