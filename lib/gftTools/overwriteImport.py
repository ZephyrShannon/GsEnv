
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

class OverwritesAtImport:
    orig_dataframe_get = pd.DataFrame.__getstate__
    orig_dataframe_set = pd.DataFrame.__setstate__
    dataframe_metas = ['last_update_time']
    def __init__(self):
        pd.DataFrame.__getstate__ = __gs_getstate__
        pd.DataFrame.__setstate__ = __gs_setstate__


start = OverwritesAtImport()



import inspect
import sys
import os


def get_lib_roots():
    path_dict = dict()
    for path in sys.path:
        path_dict[path] = len(path)
    return path_dict

class GsImport:
    def __init__(self, gs_env):
        self.gs_env = gs_env
        self.imported_set = set()
        self.user_roots = get_lib_roots()
        import builtins
        self.sys_import = builtins.__import__
        builtins.__import__ = self

    def find_relative_path(self, file_path:str):
        ret = None
        for path in self.user_roots.keys():
            if file_path.startswith(path):
                ret = path
            elif ret is not None:
                break
        if ret is not None:
            last_char = ret[len(ret)-1]
            if last_char == '/' or last_char =='\\':
                return file_path[len(ret):]
            else:
                return file_path[len(ret)+1:]
        return ret


    def __call__(self, name:str, globals=None, locals=None, fromlist=(), level=0):
        ret = self.sys_import(name, globals,locals,fromlist,level)
        self.update_module_2_neo4j(ret)
        return ret

    def update_module_2_neo4j(self, imported_item):
        if inspect.ismodule(imported_item):
            if imported_item.__name__ not in self.imported_set:
                self.imported_set.add(imported_item.__name__)
                try:
                    filepath = inspect.getfile(imported_item)
                    rel_path = self.find_relative_path(filepath)
                    # if filepath.startswith(self.user_root):
                    print("module name:" + imported_item.__name__ + ",file:" + rel_path)

                    inspect.getc

                except TypeError as te:
                    print(imported_item.__name__ + " has no file")


#gs_importer = GsImport(None)
