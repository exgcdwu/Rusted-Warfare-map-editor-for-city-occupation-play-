import numpy as np
from copy import deepcopy
from typing import Union

import rwmap._frame as frame
import rwmap._data.const as const
import rwmap._util as utility
from rwmap._exceptions import KeyConflictError, TileGroupMatrixListOfListError
from rwmap._data.const import TYPE

tilestate_type = "S20"

class TileGroup_Matrix:
    pass

class TileGroup_Matrix:
    def __init__(self, tilename_matrix:list[list]):
        self._tilematrix = deepcopy(np.array(tilename_matrix, tilestate_type))
        if len(self._tilematrix.shape) == 1:
            self._tilematrix = self._tilematrix.reshape((1, len(tilename_matrix)))
        self._size = frame.Coordinate(self._tilematrix.shape[0], self._tilematrix.shape[1])
        self._acce_dict = {}

    def tilematrix(self):
        return self._tilematrix

    def size(self)->frame.Coordinate:
        return self._size
    
    def __getitem__(self, place:frame.Coordinate)->str:
        return bytes(self._tilematrix[place.x(), place.y()]).decode("utf-8")
    
    def save_acce_s(self, map:str, gidmatrix:np.ndarray):
        self._acce_dict[map] = gidmatrix
    
    def get_acce_s(self, map:str):
        return self._acce_dict.get(map)

    def map(self, dic:dict)->TileGroup_Matrix:
        tilegroup_map = deepcopy(self)
        for place in self._size:
            value = self.__getitem__(place)
            if dic.get(value) != None:
                tilegroup_map._tilematrix[place.x()][place.y()] = deepcopy(dic[value])
        return tilegroup_map
    
    def part(self, rect:frame.Rectangle)->TileGroup_Matrix:
        tilegroup_part = deepcopy(self)
        tilegroup_part._size = deepcopy(rect._addCoordinate)
        tilegroup_part._tilematrix = deepcopy(self._tilematrix[int(rect.i().x()):int(rect.e().x()), int(rect.i().y()):int(rect.e().y())])
        return tilegroup_part
    
    def flip_h(self)->TileGroup_Matrix:
        tilegroup_part = deepcopy(self)
        tilegroup_part._tilematrix = np.flipud(tilegroup_part._tilematrix)

    def flip_v(self)->TileGroup_Matrix:
        tilegroup_part = deepcopy(self)
        tilegroup_part._tilematrix = np.fliplr(tilegroup_part._tilematrix)

    def rotate_CW(self)->TileGroup_Matrix:
        tilegroup_part = deepcopy(self)
        tilegroup_part._tilematrix = np.flipud(tilegroup_part._tilematrix.transpose())

    def rotate_RW(self)->TileGroup_Matrix:
        tilegroup_part = deepcopy(self)
        tilegroup_part._tilematrix = np.fliplr(tilegroup_part._tilematrix.transpose())
    
    def rotate_O(self)->TileGroup_Matrix:
        tilegroup_part = deepcopy(self)
        tilegroup_part._tilematrix = np.fliplr(np.flipud(tilegroup_part._tilematrix))
    
class TileGroup_AddLayer(TileGroup_Matrix):
    def __init__(self, layername:str, tilename_matrix):
        TileGroup_Matrix.__init__(self, tilename_matrix)
        TileGroup_AddLayer._add_layername(self, layername)

    def _add_layername(self, layername:str)->None:
        self._layername = layername

    @classmethod
    def init_tilegroup_matrix(cls, layername:str, tilegroup_matrix:TileGroup_Matrix):
        return cls(layername, tilegroup_matrix._tilematrix)
    
    @classmethod
    def init_tilegroup(cls, tilegroup):
        return cls(tilegroup.layername(), tilegroup.tilematrix())

    def layername(self)->str:
        return self._layername



class TileGroup_AddFile(TileGroup_Matrix):
    def __init__(self, tilename_to_tileset:dict[str, TYPE.tileid], tilename_matrix):
        TileGroup_Matrix.__init__(self, tilename_matrix)
        TileGroup_AddFile._add_tilename(self, tilename_to_tileset)

    def _add_tilename(self, tilename_to_tileset:dict[str, TYPE.tileid])->None:
        tilename_to_tileset_n = deepcopy(tilename_to_tileset)
        zeroadd = {const.KEY.empty_tile_for_tilegroup: frame.TagCoordinate.init_xy("empty", 0, 0)}
        if utility.dict_isconflict(tilename_to_tileset, zeroadd):
            raise KeyConflictError("Key-value of the tile group conflicts at instantiation. \
                                   0 is the default empty tile.")
        tilename_to_tileset_n.update(zeroadd)
        self._tilename_to_tileset = tilename_to_tileset_n

    @classmethod
    def init_tilegroup_matrix(cls, tilename_to_tileset:str, tilegroup_matrix:TileGroup_Matrix):
        return cls(tilename_to_tileset, tilegroup_matrix._tilematrix)

    def __getitem__(self, place: frame.Coordinate) -> TYPE.tileid:
        stritems = TileGroup_Matrix.__getitem__(self, place)
        if self._tilename_to_tileset.get(stritems) == None:
            return 0
        else:
            return deepcopy(self._tilename_to_tileset[stritems])
    
    def tilename_to_tileset(self)->dict[str, TYPE.tileid]:
        return deepcopy(self._tilename_to_tileset)
    
class TileGroup_One(TileGroup_AddFile, TileGroup_AddLayer):
    def __init__(self, layername:str, tilename_to_tileset:dict[str, TYPE.tileid], tilename_matrix)->None:
        TileGroup_Matrix.__init__(self, tilename_matrix)
        self._add_layername(layername)
        self._add_tilename(tilename_to_tileset)
    
    @classmethod
    def init_tilegroup_matrix(cls, layername:str, tilename_to_tileset:dict[str, TYPE.tileid], tilegroup_matrix:TileGroup_Matrix):
        return cls(layername, tilename_to_tileset, tilegroup_matrix._tilematrix)
    
    @classmethod
    def init_tilegroup_addfile(cls, layername:str, tilegroup_addfile:TileGroup_AddFile):
        return cls(layername, tilegroup_addfile._tilename_to_tileset, tilegroup_addfile._tilematrix)

    @classmethod
    def init_tilegroup_addlayer(cls, tilename_to_tileset:dict[str, TYPE.tileid], tilegroup_addlayer:TileGroup_AddLayer):
        return cls(tilegroup_addlayer._layername, tilename_to_tileset, tilegroup_addlayer._tilematrix)

class TileGroup_List_SubTileName:
    def __init__(self, tilegrouplist_addlayer:list[TileGroup_AddLayer]):
        self._tilegrouplist_addlayer = deepcopy(tilegrouplist_addlayer)

    def tilegrouplist(self):
        return deepcopy(self._tilegrouplist_addlayer)

class TileGroup_List(TileGroup_List_SubTileName):
    def __init__(self, tilename_to_tileset:dict[str, TYPE.tileid], tilegrouplist_addlayer:list[TileGroup_AddLayer]):
        TileGroup_List_SubTileName.__init__(self, tilegrouplist_addlayer)
        self._add_tilename(tilename_to_tileset)

    def _add_tilename(self, tilename_to_tileset:dict[str, TYPE.tileid])->None:
        self._tilename_to_tileset = deepcopy(tilename_to_tileset)

    @classmethod
    def init_tilegroup_list_subtilename(cls, tilename_to_tileset:dict[str, TYPE.tileid], tilegrouplist_subtilename:TileGroup_List_SubTileName):
        return cls(tilename_to_tileset, tilegrouplist_subtilename.tilegrouplist())

    @classmethod
    def init_tilegroup_list(cls, tilegrouplist:list[TileGroup_One]):
        tilegrouplist_addlayer = []
        tilename_to_tileset = {}
        for tilegroup in tilegrouplist:
            dict_new = tilegroup.tilename_to_tileset()
            del dict_new[const.KEY.empty_tile_for_tilegroup]
            if utility.dict_isconflict(tilename_to_tileset, dict_new):
                raise KeyConflictError("Key-value of the tile group conflicts at instantiation.")
            tilename_to_tileset.update(dict_new)
            tilegrouplist_addlayer.append(TileGroup_AddLayer.init_tilegroup(tilegroup))
        return cls(tilename_to_tileset, tilegrouplist_addlayer)

    def _iterator(self):
        for tilegroup in self._tilegrouplist_addlayer:
            yield TileGroup_One.init_tilegroup_addlayer(self._tilename_to_tileset, tilegroup)

    def __iter__(self):
        return self._iterator()