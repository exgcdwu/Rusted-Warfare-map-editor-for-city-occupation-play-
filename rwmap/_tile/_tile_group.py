import numpy as np

import rwmap._frame as frame
import rwmap._util as utility
from rwmap._exceptions import KeyConflictError

tilestate_type = "S20"

class TileGroup_Matrix:
    def __init__(self, tilename_matrix):
        self._tilematrix = np.array(tilename_matrix, tilestate_type)
        self._size = frame.Coordinate(self._tilematrix.shape[0], self._tilematrix.shape[1])

    def tilematrix(self):
        return self._tilematrix

    def size(self)->frame.Coordinate:
        return self._size
    
    def __getitem__(self, place:frame.Coordinate)->str:
        return self._tilematrix[place.x()][place.y()]
    
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
    def __init__(self, tilename_to_tileset:dict[str, frame.TagCoordinate], tilename_matrix):
        TileGroup_Matrix.__init__(self, tilename_matrix)
        TileGroup_AddFile._add_tilename(self, tilename_to_tileset)

    def _add_tilename(self, tilename_to_tileset:dict[str, frame.TagCoordinate])->None:
        zeroadd = {"0": frame.TagCoordinate.init_xy("empty", 0, 0)}
        if utility.dict_isconflict(tilename_to_tileset, zeroadd):
            raise KeyConflictError("Key-value of the tile group conflicts at instantiation. \
                                   0 is the default empty tile.")
        tilename_to_tileset.update(zeroadd)
        self._tilename_to_tileset = tilename_to_tileset

    @classmethod
    def init_tilegroup_matrix(cls, tilename_to_tileset:str, tilegroup_matrix:TileGroup_Matrix):
        return cls(tilename_to_tileset, tilegroup_matrix._tilematrix)

    def __getitem__(self, place: frame.Coordinate) -> frame.TagCoordinate:
        stritems = bytes(TileGroup_Matrix.__getitem__(self, place)).decode("utf-8")
        return self._tilename_to_tileset[stritems]
    
    def tilename_to_tileset(self)->dict[str, frame.TagCoordinate]:
        return self._tilename_to_tileset
    
class TileGroup_One(TileGroup_AddFile, TileGroup_AddLayer):
    def __init__(self, layername:str, tilename_to_tileset:dict[str, frame.TagCoordinate], tilename_matrix)->None:
        TileGroup_Matrix.__init__(self, tilename_matrix)
        self._add_layername(layername)
        self._add_tilename(tilename_to_tileset)
    
    @classmethod
    def init_tilegroup_matrix(cls, layername:str, tilename_to_tileset:dict[str, frame.TagCoordinate], tilegroup_matrix:TileGroup_Matrix):
        return cls(layername, tilename_to_tileset, tilegroup_matrix._tilematrix)
    
    @classmethod
    def init_tilegroup_addfile(cls, layername:str, tilegroup_addfile:TileGroup_AddFile):
        return cls(layername, tilegroup_addfile._tilename_to_tileset, tilegroup_addfile._tilematrix)

    @classmethod
    def init_tilegroup_addlayer(cls, tilename_to_tileset:dict[str, frame.TagCoordinate], tilegroup_addlayer:TileGroup_AddLayer):
        return cls(tilegroup_addlayer._layername, tilename_to_tileset, tilegroup_addlayer._tilematrix)

class TileGroup_List_SubTileName:
    def __init__(self, tilegrouplist_addlayer:list[TileGroup_AddLayer]):
        self._tilegrouplist_addlayer = tilegrouplist_addlayer

    def tilegrouplist(self):
        return self._tilegrouplist_addlayer

class TileGroup_List(TileGroup_List_SubTileName):
    def __init__(self, tilename_to_tileset:dict[str, frame.TagCoordinate], tilegrouplist_addlayer:list[TileGroup_AddLayer]):
        super().__init__(self, tilegrouplist_addlayer)
        self._add_tilename(tilename_to_tileset)

    def _add_tilename(self, tilename_to_tileset:dict[str, frame.TagCoordinate])->None:
        self._tilename_to_tileset = tilename_to_tileset

    @classmethod
    def init_tilegroup_list_subtilename(cls, tilename_to_tileset:dict[str, frame.TagCoordinate], tilegrouplist_subtilename:TileGroup_List_SubTileName):
        return cls(tilename_to_tileset, tilegrouplist_subtilename.tilegrouplist())

    @classmethod
    def init_tilegroup_list(cls, tilegrouplist:list[TileGroup_One]):
        tilegrouplist_addlayer = []
        tilename_to_tileset = {}
        for tilegroup in tilegrouplist:
            if utility.dict_isconflict(tilename_to_tileset, tilegroup.tilename_to_tileset()):
                raise KeyConflictError("Key-value of the tile group conflicts at instantiation.")
            tilename_to_tileset.update(tilegroup.tilename_to_tileset())
            tilegrouplist_addlayer.append(TileGroup_AddLayer.init_tilegroup(tilegroup))
        return cls(tilename_to_tileset, tilegrouplist_addlayer)

    def __next__(self):
        for tilegroup in self._tilegrouplist_addlayer:
            yield TileGroup_One.init_tilegroup_addlayer(self._tilename_to_tileset, tilegroup)

    def __iter__(self):
        return self