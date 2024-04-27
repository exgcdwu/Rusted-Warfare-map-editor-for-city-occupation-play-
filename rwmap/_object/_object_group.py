from copy import deepcopy

import rwmap._frame as frame

from rwmap._object._object_one_and_acti import TObject_One

class TObject_Group:
    pass

class TObject_Group:
    def __init__(self, TObject_One_list:list[TObject_One], TObject_Group_list:list[TObject_Group] = []):
        self._TObject_One_list = [deepcopy(TObject) for TObject in TObject_One_list]
        self._TObject_Group_list = [deepcopy(TObject_Groupn) for TObject_Groupn in TObject_Group_list]

    def offset(self, offset:frame.Coordinate)->TObject_Group:
        ntob = deepcopy(self)
        for tob in ntob._TObject_One_list:
            tob._pos = tob.offset(offset)
        for tobg in ntob._TObject_Group_list:
            tobg.offset(offset)
        return ntob