
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
        print("import"+name)
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


                except TypeError as te:
                    print(imported_item.__name__ + " has no file")

import inspect
from lib.gftTools.proto import pythonLibInspect_pb2 as libInspect


def find_module_member(mb_list):
    idx = 0
    for key, item in mb_list:
        if inspect.ismodule(item):
            print("[{0}]:{1}".format(str(idx), item.__name__))
            # return item
        idx += 1


def print_sub_modules(module_data):
    print("module:" + module_data.name)
    idx = 0
    for mod in module_data.sub_modules:
        print("sub module" + str(idx) + ":" + mod.name)
        idx += 1
    idx = 0
    for cla in module_data.class_defs:
        print("sub class:" + str(idx) + ":" + cla.name)
        idx += 1


def print_class(cla_data):
    print("class:" + cla_data.name)
    idx = 0
    for cla in cla_data.sub_classes:
        print("  sub class" + str(idx) + ":" + cla.name)
        idx += 1
    idx = 0
    for method in cla_data.methods:
        print(" method:" + str(idx) + ":" + method.name)
        idx += 1


def find_member(mb_list, key_name):
    idx = 0
    for key, item in mb_list:
        if key == key_name:
            print(idx)
            return item
        idx += 1


class moduleImporter:
    def __init__(self):
        self.layer = 0
        self.file_handle = None

    def open_file(self , file_name):
        self.file_handle = open(file_name)

    def close_file(self):
        self.file_handle.close()

    def print_tree(self , name, type):
        return
        prefix = ""
        for i in range(self.layer):
            prefix += '    '
        print("{0}{1}[{2}]".format(prefix, name, type))

    def __get_full_path__(self , val):
        if hasattr(val, '__module__') and hasattr(val, '__name__'):
            return "{0}.{1}".format(val.__module__, val.__name__)
        else:
            return str(type(val))

    def __test_scalar_type__(self , value):
        if value is None:
            return 0
        val_type = type(value)
        if (val_type == str) or (val_type == int) or (val_type == float) or (val_type == bool):
            return 1
        return -1

    def __extract_value__(self , value, add_into):
        if value is None:
            add_into.is_none = True
            return

        val_type = type(value)
        if val_type == str:
            add_into.str_val = value
        elif val_type == int:
            add_into.int_val = value
        elif val_type == float:
            add_into.float_val = value
        elif val_type == bool:
            add_into.boolean_val = value
        else:
            add_into.other_type = self.__get_full_path__(value)

    def __extract_basic_info__(self , obj, add_into):
        add_into.name = obj.__name__
        doc = inspect.getdoc(obj)
        if doc:
            add_into.doc = doc
        comments = inspect.getcomments(obj)
        if comments:
            add_into.comments = comments

    def __dont_export_obj__(self, obj):
        comments = inspect.getcomments(obj)
        if comments:
            if '$do not export$' in comments:
                print(obj.__name__ + " is omited")
                return True
        return False

    SA_PARAMETER_TYPE_INT = 1
    SA_PARAMETER_TYPE_VALUE = 2
    SA_PARAMETER_TYPE_STRING = 3
    SA_PARAMETER_TYPE_J_ARRAY = 11
    SA_PARAMETER_TYPE_J_DICTIONARY = 14
    SA_PARAMETER_TYPE_USE_INSTRUCTION_OUTPUT = 20

    def __get_func_type_enum_val__(self , par):
        if par._kind == inspect._VAR_POSITIONAL:
            return moduleImporter.SA_PARAMETER_TYPE_J_ARRAY
        elif par._kind == inspect._VAR_KEYWORD:
            return moduleImporter.SA_PARAMETER_TYPE_J_DICTIONARY
        return self.__get_func_type__( par.annotation)

    def __get_func_type__(self , type):
        if type == int:
            return moduleImporter.SA_PARAMETER_TYPE_INT
        elif type == float:
            return moduleImporter.SA_PARAMETER_TYPE_VALUE
        elif type == str:
            return moduleImporter.SA_PARAMETER_TYPE_STRING
        else:
            return moduleImporter.SA_PARAMETER_TYPE_USE_INSTRUCTION_OUTPUT

    EN_PTYHON_TYPE_MODULE = 0
    EN_PYTHON_TYPE_CLASS = 1
    EN_PYTHON_TYPE_FUNC = 2
    EN_PYTHON_TYPE_SCALAR = 3

    def __add_reference_info__(self , obj, showname: str, reference_data: libInspect.reference_info):
        reference_data.showname = showname
        if inspect.isclass(obj):
            name = "{0}.{1}".format(obj.__module__, obj.__name__)
            reference_data.name = name
            reference_data.type = moduleImporter.EN_PYTHON_TYPE_CLASS
        elif inspect.ismodule(obj):
            reference_data.name = obj.__name__
            reference_data.type = moduleImporter.EN_PTYHON_TYPE_MODULE
        elif inspect.isfunction(obj):
            reference_data.name = '{0}.{1}'.format(obj.__module__, obj.__qualname__)
            reference_data.type = moduleImporter.EN_PYTHON_TYPE_FUNC
        else:
            reference_data.name = '{0}.{1}'.format(obj.__module__, obj.__name__)
            reference_data.type = moduleImporter.EN_PYTHON_TYPE_SCALAR

    def __extract_fucntion_info__(self , function_obj, func_data: libInspect.function_info, is_bound_func, is_in_class):
        # if not isinstance(func_obj, function):
        #     raise Exception("Not a function")
        self.__extract_basic_info__( function_obj, func_data)
        self.print_tree(func_data.name, 'func')
        func_data.is_bound_method = is_bound_func
        sign = inspect.signature(function_obj)
        idx = 0
        no_self_par = True

        for key, val in sign.parameters.items():
            if 0 == idx:
                if key == 'self':
                    no_self_par = False
            par = func_data.sign.paras.add()
            par.name = key
            par.idx = idx
            idx += 1
            par.type = self.__get_func_type_enum_val__(val)
            if type(inspect._empty) != type(val.default) or inspect._empty != val.default:
                self.__extract_value__( val.default, par.default_val)

        if is_in_class and no_self_par:
            func_data.is_bound_method = True

        return func_data

    def __not_in_module__(self , obj, module_name):
        if inspect.isfunction(obj):
            return not obj.__module__.startswith(module_name)
        name = getattr(obj, "__name__", None)
        if name is None:
            return True

        if inspect.isclass(obj):
            module = getattr(obj, "__module__", None)
            if module is None:
                return True
            return not module.startswith(module_name)
        elif inspect.ismodule(obj):
            return not obj.__name__.startswith(module_name)
        else:
            return True

    def get_func_parent(self , func_obj):
        if func_obj.__qualname__ != func_obj.__name__:
            if func_obj.__qualname__.endswith(func_obj.__name__):
                parent_class = func_obj.__qualname__[:func_obj.__qualname__.index(func_obj.__name__) - 1]
                return func_obj.__module__ + "." + parent_class
            else:
                return "Drop it!"  # mean drop it.
        return func_obj.__module__

    def __extract_class_info__(self , cls_obj, module_name: str, class_data: libInspect.class_info, omit_dict: dict):
        # if not isinstance(cls_obj, type):
        #     raise Exception("Not a class")
        self.__extract_basic_info__( cls_obj, class_data)
        class_path = cls_obj.__module__ + "." + cls_obj.__name__
        #
        # supers = inspect.getmro(cls_obj)
        # if len(supers) > 2:
        #     for i in range(1, len(supers)-1):
        #         super_class =  supers[i]
        #         class_data.super_classes.append(super_class.__module__ + "." + super_class.__name__)

        self.print_tree(class_data.name, 'class')
        self.layer += 1
        member_list = inspect.getmembers(cls_obj)
        for name, val in member_list:
            if name.startswith("__") and (name != '__init__'):
                continue
            if self.__not_in_module__(val, module_name):
                continue
            if self.__dont_export_obj__(val):
                continue
            if omit_dict is None:
                choice = None
            else:
                choice = omit_dict.get(name)
            if isinstance(choice, int):
                if choice == 0:  # mean omit it.
                    continue
                if choice == 1:
                    ref = class_data.references.add()
                    self.__add_reference_info__( val, name, ref)

            if inspect.isfunction(val):
                if inspect.isbuiltin(val):
                    continue
                full_path = "{0}.{1}".format(val.__module__, val.__qualname__)
                if omit_dict.__contains__(full_path):
                    ref = class_data.references.add()
                    self.__add_reference_info__( val, name, ref)
                else:
                    omit_dict[full_path] = 1

                if class_path == self.get_func_parent( val):
                    func_data = class_data.methods.add()
                    self.__extract_fucntion_info__( val, func_data, False, True)
            elif inspect.ismethod(val):
                if omit_dict.__contains__(full_path):
                    ref = class_data.references.add()
                    self.__add_reference_info__( val, name, ref)
                else:
                    omit_dict[full_path] = 1
                if class_path == self.get_func_parent( val):
                    func_data = class_data.methods.add()
                    self.__extract_fucntion_info__( val, func_data, True, True)
            elif inspect.isclass(val):
                print("Find sub class:" + name + ":" + str(val) + " my name:" + str(cls_obj))
                ref = class_data.references.add()
                self.__add_reference_info__( val, name, ref)
                # full_path = "{0}.{1}".format(val.__module__, val.__name__)
                # if omit_dict.__contains__(full_path):
                #     ref = class_data.references.add()
                #     self.__add_reference_info__( val, name, ref)
                # else:
                #     omit_dict[full_path] = 1
                # sub_class_data = class_data.sub_classes.add()
                # self.__extract_class_info__(val, module_name, sub_class_data, omit_dict)
            else:
                scalar_type = self.__test_scalar_type__(val)
                if scalar_type >= 0:
                    par = class_data.enum_defs.add()
                    par.name = name
                    self.__extract_value__( val, par.default_val)

        self.layer -= 1
        return class_data



    def should_omit(self , name):
        if name.startswith("_") and (name != '__init__'):
            # print("omit:"+name)
            return True
        if name.endswith('deprecated'):
            # print("omit:" + name)
            return True

    def __extract_module_info__(self , module_obj, showname: str, module_name: str, module_data: libInspect.module_info,
                                omit_dict: set):
        # if not isinstance(lib_obj, module):
        #     raise Exception("Not a module")
        self.__extract_basic_info__( module_obj, module_data)
        if showname:
            module_data.showname = showname
        self.print_tree(module_data.name, 'module')
        self.layer += 1
        member_list = inspect.getmembers(module_obj)
        if hasattr(module_obj, "__version__"):
            module_data.version = str(module_obj.__version__)
        # module_data.file_name = inspect.getfile(module_obj)
        for name, val in member_list:
            if self.should_omit(name):
                continue;
            if omit_dict is None:
                choice = None
            else:
                choice = omit_dict.get(name)
            if isinstance(choice, int):
                if choice == 0:  # mean omit it.
                    continue
                if choice == 1:
                    ref = module_data.references.add()
                    self.__add_reference_info__( val, name, ref)
            if self.__not_in_module__(val, module_name):
                continue
            if self.__dont_export_obj__(val):
                continue
            if inspect.ismodule(val):
                if omit_dict.__contains__(val.__name__):
                    continue
                omit_dict[val.__name__] = 1
                sub_module_data = module_data.sub_modules.add()
                self.__extract_module_info__(val, name, module_name, sub_module_data, omit_dict)
            elif inspect.isfunction(val):
                full_path = "{0}.{1}".format(val.__module__, val.__qualname__)
                if omit_dict.__contains__(full_path):
                    ref = module_data.references.add()
                    self.__add_reference_info__( val, name, ref)
                else:
                    omit_dict[full_path] = 1

                if inspect.isbuiltin(val):
                    continue
                if module_obj.__name__ == self.get_func_parent( val):
                    func_data = module_data.funcs.add()
                    self.__extract_fucntion_info__( val, func_data, False, False)
                else:
                    ref = module_data.references.add()
                    self.__add_reference_info__( val, name, ref)

            elif inspect.isclass(val):
                full_path = "{0}.{1}".format(val.__module__, val.__name__)
                if omit_dict.__contains__(full_path):
                    ref = module_data.references.add()
                    self.__add_reference_info__( val, name, ref)
                else:
                    omit_dict[full_path] = 1

                if val.__module__ == module_obj.__name__:
                    class_data = module_data.class_defs.add()
                    self.__extract_class_info__(val, module_name, class_data, omit_dict)
                else:
                    ref = module_data.references.add()
                    self.__add_reference_info__( val, name, ref)
            else:
                full_path = "{0}.{1}".format(val.__module__, val.__name__)
                if omit_dict.__contains__(full_path):
                    ref = module_data.references.add()
                    self.__add_reference_info__( val, name, ref)
                else:
                    omit_dict[full_path] = 1

                scalar_type = self.__test_scalar_type__(val)
                if scalar_type >= 0:
                    par = class_data.enum_defs.add()
                    par.name = name
                    self.__extract_value__( val, par.default_val)

        self.layer -= 1
        return module_data

    def __extract_name_and_module__(self , obj, module_data):
        package = obj.__package__
        package_path = package.split('.')
        path_len = len(package_path)
        if path_len > 1:
            module_data.from_packages.extend(package_path[:-1])
        module_data.name = package_path[-1]

    def extract_info(self , target_obj, showname=None, omit_dict: dict = dict()):
        ret = libInspect.module_info()
        if inspect.ismodule(target_obj):
            self.__extract_module_info__(target_obj, showname, target_obj.__name__, ret, omit_dict)
            package = target_obj.__package__
            if package:
                package_path = package.split('.')
                ret.from_packages.extend(package_path)
            return ret
        elif inspect.isfunction(target_obj):
            self.__extract_name_and_module__(target_obj, ret)
            func_data = ret.funcs.add()
            self.__extract_fucntion_info__( target_obj, target_obj.__module__, func_data, False, False)
        elif inspect.isclass(target_obj):
            self.__extract_name_and_module__(target_obj, ret)
            class_data = ret.class_defs.add()
            self.__extract_class_info__(target_obj, target_obj.__module__, class_data, omit_dict)
        return ret

    def keep_func(self , func_data: libInspect.function_info):
        if func_data.HasField('sign'):
            sign = func_data.sign
            for par in sign.paras:
                if par.type == SA_PARAMETER_TYPE_J_DICTIONARY:
                    print("Keep func:" + func_data.name)
                    return True
        return False

    def filter_class(self , class_data: libInspect.class_info):
        rem_list = list()
        print('filter class' + class_data.name)
        for func in class_data.methods:
            if not self.keep_func(func):
                rem_list.append(func)
        for func in rem_list:
            class_data.methods.remove(func)
        class_data.ClearField('references')

    def filter_module(self , module_data: libInspect.module_info):
        print("filter module" + module_data.name)
        for class_data in module_data.class_defs:
            self.filter_class(class_data)
        rem_list = list()
        for sub_module in module_data.sub_modules:
            self.filter_module(sub_module)

        for func in module_data.funcs:
            if not self.keep_func(func):
                rem_list.append(func)
        for func in rem_list:
            module_data.funcs.remove(func)
        module_data.ClearField('references')




gs_importer = GsImport(None)

# mod_imp = moduleImporter()

from lib.gftTools import gftIO