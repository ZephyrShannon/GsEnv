
import pandas as pd
def __gs_getstate__(self):
    # print("gs get state is called!")
    orig_dic = OverwriteImport.orig_dataframe_get(self)
    for key in OverwriteImport.dataframe_metas:
        val = self.__dict__.get(key, None)
        if val is not None:
            orig_dic[key] = val
    return orig_dic


def __gs_setstate__(self, state: dict):
    # print("gs set state is called!")
    for key in OverwriteImport.dataframe_metas:
        val = state.pop(key, None)
        if val is not None:
            self.__dict__[key] = val
    OverwriteImport.orig_dataframe_set(self, state)

class OverwriteImport:
    orig_dataframe_get = pd.DataFrame.__getstate__
    orig_dataframe_set = pd.DataFrame.__setstate__
    dataframe_metas = ['last_update_time']
    def __init__(self):
        pd.DataFrame.__getstate__ = __gs_getstate__
        pd.DataFrame.__setstate__ = __gs_setstate__


start = OverwriteImport()

