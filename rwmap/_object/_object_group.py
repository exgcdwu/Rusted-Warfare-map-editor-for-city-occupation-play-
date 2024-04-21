from copy import deepcopy

import rwmap._frame as frame

from rwmap._object._object_one_and_acti import TObject_One

class TObject_Group:
    pass

class TObject_Group:
    def __init__(self, TObject_One_list:list[TObject_One], TObject_Group_list:list[TObject_Group] = []):
        self._TObject_One_list = TObject_One_list
        for tobject_group in TObject_Group_list:
            self._TObject_One_list = self._TObject_One_list + tobject_group._TObject_One_list

    def offset(self, offset:frame.Coordinate)->TObject_Group:
        ntob = deepcopy(self)
        for tob in ntob._TObject_One_list:
            tob._pos = tob.offset(offset)
        return ntob