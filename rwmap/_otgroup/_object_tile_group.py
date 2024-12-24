from copy import deepcopy

import rwmap._frame as frame

from rwmap._object._object_group import TObject_Group
from rwmap._tile._tile_group import TileGroup_List

class OTGroup:
    pass

class OTGroup:
    def __init__(self, tobject_group:TObject_Group, tilegroup_list:TileGroup_List):
        self._tobject_group = tobject_group
        self._tilegroup_list = tilegroup_list
