import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY
from auto._data._const import *
from auto._data._object import *

dictionary_info_args_dict = OrderedDict()

dictionary_info_args_dict[INFOKEY.prefix] = str
dictionary_info_args_dict[INFOKEY.cite_name] = str
dictionary_info_args_dict[INFOKEY.isprefixseg] = bool
dictionary_info_args_dict[INFOKEY.brace] = (list, str)

dictionary_info_optional_set = {
    INFOKEY.brace
}

dictionary_info_default_args_dict = {
    INFOKEY.isprefixseg: "true", 
}

dictionary_info = {
    INFOKEY.dictionary_info:{
        AUTOKEY.info_args:dictionary_info_args_dict, 
        AUTOKEY.default_args: dictionary_info_default_args_dict, 
        AUTOKEY.optional: dictionary_info_optional_set, 
        AUTOKEY.args: [
            ("cite_name", str)
        ], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.operation:BRACE_OPERATION_END, 
        AUTOKEY.no_check: True
    }
}