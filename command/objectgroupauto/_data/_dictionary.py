import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._data._const import *
from command.objectgroupauto._data._object import *

dictionary_info_args_dict = OrderedDict()

dictionary_info_args_dict[INFOKEY.prefix] = str
dictionary_info_args_dict[INFOKEY.cite_name] = str
dictionary_info_args_dict[INFOKEY.isprefixseg] = bool

dictionary_info_optional_set = set()

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
        AUTOKEY.operation:[], 
        AUTOKEY.no_check: True, 
        AUTOKEY.isnot_cite_check: True
    }
}

dictionary_info = brace_add_info(dictionary_info)