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

bdtext_info_args_dict = OrderedDict()

bdtext_info_args_dict[INFOKEY.prefix] = str
bdtext_info_args_dict[INFOKEY.isbdtext] = bool
bdtext_info_args_dict[INFOKEY.bdcolor] = str
bdtext_info_args_dict[INFOKEY.bdtextsize] = str
bdtext_info_args_dict[INFOKEY.bdtext] = str
bdtext_info_args_dict[INFOKEY.bdname] = str
bdtext_info_args_dict[INFOKEY.bdoffset] = (list, int)
bdtext_info_args_dict[INFOKEY.bdoffsetsize] = (list, int)

bdtext_info_default_args_dict = {
    INFOKEY.isbdtext: "true",  
    INFOKEY.bdname: "", 
    INFOKEY.bdoffset: "0 0", 
    INFOKEY.bdoffsetsize: "0 0"
}

bdtext_info_var_dependent_dict = {
    INFOKEY.bdcolor: INFOKEY.isbdtext, 
    INFOKEY.bdtextsize: INFOKEY.isbdtext, 
    INFOKEY.bdname: INFOKEY.isbdtext, 
    INFOKEY.bdoffset: INFOKEY.isbdtext, 
    INFOKEY.bdoffsetsize: INFOKEY.isbdtext, 
    INFOKEY.bdtext: INFOKEY.isbdtext, 
}

bdtext_info_optional_set = {
    INFOKEY.isbdtext, INFOKEY.bdcolor, INFOKEY.bdtextsize, INFOKEY.bdname, 
    INFOKEY.bdoffset, INFOKEY.bdoffsetsize
}

bdtext_info_operation_list = \
    operation_if(INFOKEY.isbdtext, "bdtext_if_isbdtext") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.offset: f"{INFOKEY.bdoffset}", 
                AUTOKEY.offsetsize: f"{INFOKEY.bdoffsetsize}", 
                AUTOKEY.name: "{" + f"{INFOKEY.bdname}" + "}", 
                AUTOKEY.type: rw.const.OBJECTTYPE.mapText, 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.text: "{" + f"{INFOKEY.bdtext}" + "}", 
                    rw.const.OBJECTOP.textColor: ("{" + f"{INFOKEY.bdcolor}" + "}", "bdcolor", AUTOKEY.exist), 
                    rw.const.OBJECTOP.textSize: ("{" + f"{INFOKEY.bdtextsize}" + "}", "bdtextsize", AUTOKEY.exist), 
                }
            }
        ] + \
    operation_ifend("bdtext_if_isbdtext")


bdtext_info = {
    INFOKEY.bdtext_info:{
        AUTOKEY.info_args:bdtext_info_args_dict, 
        AUTOKEY.default_args:bdtext_info_default_args_dict, 
        AUTOKEY.optional: bdtext_info_optional_set, 
        AUTOKEY.prefix: INFOKEY.prefix, 
        AUTOKEY.isinfo_sub: True
    }
}