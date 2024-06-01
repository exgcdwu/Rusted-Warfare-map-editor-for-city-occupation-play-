# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
from copy import deepcopy
import numpy as np
import os
import base64

import rwmap._util as utility
import rwmap._frame as frame
import rwmap._data.const as const
import rwmap._exceptions as exception
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties

class TileSet(ElementOri):
    def __init__(self, properties:ElementProperties, size:frame.Coordinate, image_properties:ElementProperties = None,
                  png_text:str = None, tilelist_properties:list[ElementProperties] = None, coo_to_tileid_matrix:np.ndarray = None, 
                  tileid_to_coo_list:list[frame.Coordinate] = None)->None:
        super().__init__(properties)
        self._size = deepcopy(size)
        self._image_properties = deepcopy(image_properties)
        self._png_text = deepcopy(png_text)
        self._tilelist_properties = deepcopy(tilelist_properties)
        self._coo_to_tileid_matrix = deepcopy(coo_to_tileid_matrix)
        self._tileid_to_coo_list = deepcopy(tileid_to_coo_list)
    @classmethod
    def init_etElement(cls, root:et.Element, rwmaps_dir:str, istilesort:bool = True)->None:
        png_text_pro = utility.get_etElement_callable_from_tag_s(root, "properties")
        png_text = utility.get_etElement_name_to_text_s(png_text_pro, "embedded_png")
        properties = ElementProperties.init_etElement(root)
        if png_text != None:
            properties.deleteOptionalProperty("embedded_png")
        image_properties = ElementProperties.init_etElement(utility.get_etElement_callable_from_tag_s(root, "image"))
        tilelist_properties = [ElementProperties.init_etElement(tile) for tile in root if tile.tag == "tile"]
        tilelist_properties = None if tilelist_properties == [] else tilelist_properties
        
        if tilelist_properties != None and istilesort:
            tilelist_properties.sort()

        if properties.returnDefaultProperty("columns") == None:

            source_file = properties.returnDefaultProperty("source")
            source_list = source_file.split("/")
            source_list = source_list[utility.search_list_to_index(source_list, "maps") + 1:]
            source_list = source_list[utility.search_list_to_index(source_list, "tilesets") + 1:]
            source_file = "/".join(source_list)
            source = rwmaps_dir + source_file

            root = et.ElementTree(file = source).getroot()
            tilewidth = int(root.attrib["tilewidth"])
            tileheight = int(root.attrib["tileheight"])

            if root.attrib.get("columns") == None:
                image_element = utility.get_etElement_callable_from_tag_s(root, "image")
                image_file = rwmaps_dir + "bitmaps/" + image_element.attrib["source"].split("/")[-1]
                width = utility.image_width(image_file)
                height = utility.image_height(image_file)

                column = int(width / tilewidth)
                row = int(height / tileheight)
            else:
                column = int(root.attrib["columns"])
                row = int(int(root.attrib["tilecount"]) / column)

        else:
            column = int(properties.returnDefaultProperty("columns"))
            row = int(int(properties.returnDefaultProperty("tilecount")) / column)

        size = frame.Coordinate(row, column)

        coo_to_tileid_matrix = None
        tileid_to_coo_list = None
        
        if tilelist_properties != None and (not istilesort):
            has_pro_tileid = np.zeros([size.x(), size.y()], dtype = np.bool_)
            pre = -1
            isneed_matrix = False
            
            for tilenow in tilelist_properties:
                tileid = int(tilenow.returnDefaultProperty("id"))
                if tileid > pre:
                    pre = tileid
                else:
                    isneed_matrix = True
                coo = frame.Coordinate.init_id(tileid, size.y())
                has_pro_tileid[coo.x(), coo.y()] = True
            
            if isneed_matrix:
                coo_to_tileid_matrix = np.ndarray([size.x(), size.y()], dtype = np.uint32)
                for coo in size:
                    coo_to_tileid_matrix[coo.x(), coo.y()] = coo.id(size.y())

                tileid_to_coo_list = list(range(size.x() * size.y()))
                tilelist_index = 0
                for coo in size:
                    if has_pro_tileid[coo.x(), coo.y()]:
                        coo_to_tileid_matrix[coo.x(), coo.y()] = \
                            int(tilelist_properties[tilelist_index].returnDefaultProperty("id"))
                        tilelist_index = tilelist_index + 1
                
                for coo in size:
                    tileid_to_coo_list[coo_to_tileid_matrix[coo.x()][coo.y()]] = coo
            
        

        return cls(properties, size, image_properties, png_text, tilelist_properties, coo_to_tileid_matrix, tileid_to_coo_list)
    
    def output_str(self, pngtextnum:int = -1, tilenum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        if self._image_properties != None:
            str_ans = str_ans + self._image_properties.output_str() + "\n"
        if self._png_text != None:
            _png_text_now = self._png_text[:pngtextnum] if pngtextnum != -1 else ""
            str_ans = str_ans + _png_text_now + "\n"
        if self._tilelist_properties != None:
            str_ans = str_ans + "".join([self._tilelist_properties[i].output_str() + "\n" for i in range(0, min(tilenum, len(self._tilelist_properties)))]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans
    
    def __repr__(self)->str:
        return self.output_str()

    def output_etElement(self)->et.Element:
        root = et.Element("tileset")
        root = self._properties.output_etElement(root)
        if self._png_text != None:
            png_element = et.Element("property", {"name": "embedded_png"})
            png_element.text = self._png_text
            properties = utility.get_etElement_callable_from_tag_s(root, "properties")
            if properties == None:
                properties = et.Element("properties")
                root.append(properties)
            properties.insert(0, png_element)
        if self._image_properties != None:
            image_element = et.Element("image")
            image_element = self._image_properties.output_etElement(image_element)
            root.append(image_element)
        if self._tilelist_properties != None:
            for tile in self._tilelist_properties:
                tile_element = et.Element("tile")
                tile_element = tile.output_etElement(tile_element)
                root.append(tile_element)
        return root
    
    def write_png(self, dir:str)->None:
        if self._image_properties != None:
            pngbyte = base64.b64decode(self._png_text.encode('utf-8'))
            file_path = dir + '/' + self._image_properties.returnDefaultProperty("source")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as file_now:
                file_now.write(pngbyte)

    
    def name(self)->str:
        tileset_name = self._properties.returnDefaultProperty("name")
        if tileset_name == None:
            tileset_name = self._properties.returnDefaultProperty("source")
            tileset_name = utility.str_slash_to_dot(tileset_name)
        return tileset_name

    def change_name(self, new_name:str)->None:
        tileset_name = self._properties.returnDefaultProperty("name")
        if tileset_name != None:
            self._properties.assignDefaultProperty("name", new_name)

        tileset_name = self._properties.returnDefaultProperty("source")
        if tileset_name != None:
            tileset_name_len = len(utility.str_slash_to_dot(tileset_name))
            self._properties.assignDefaultProperty("source", tileset_name[0:-tileset_name_len-4] + new_name + ".tmx")

        tileset_name = self._image_properties.returnDefaultProperty("source")
        if tileset_name != None:
            self._image_properties.assignDefaultProperty("source", tileset_name[0:-tileset_name_len-4] + new_name + ".png")
    
    def totalgid(self)->int:
        return self._size.x() * self._size.y()

    def firstgid(self)->int:
        return int(self._properties.returnDefaultProperty("firstgid"))
    
    def endgid(self)->int:
        return self.firstgid() + self.totalgid()
    
    def changefirstgid(self, firstgid:int)->None:
        self._properties.assignDefaultProperty("firstgid", str(firstgid))

    def gid_to_tileid(self, gid:int)->tuple[str, int]:
        tileid = gid - self.firstgid()
        if tileid < 0:
            raise IndexError("The gid cannot be loaded into the current tileset.")
        return (self.name(), gid - self.firstgid())
    
    def tileid_to_gid(self, tileid:int)->int:
        return self.firstgid() + tileid
    
    def tileid_to_coo(self, tileid:int, isre:bool = True)->frame.TagCoordinate:
        if tileid < self.totalgid:
            if self._tileid_to_coo_list != None:
                if isre:
                    tagcoo = frame.TagCoordinate(self.name(), self._tileid_to_coo_list[tileid])
                else:
                    tagcoo = frame.TagCoordinate(self.name() + const.KEY.tag_for_tile_notre, self._tileid_to_coo_list[tileid])
            else:
                if isre:
                    tagcoo = frame.TagCoordinate(self.name(), self._tileid_to_coo_list[tileid])
                else:
                    raise TypeError(f"tileid_to_coo:error transfromation")                    
        else:
            raise exception.CoordinateIndexError(f"Beyond the boundary of this tileset{self.name()}")
        return tagcoo

    def coo_to_tileid(self, tile_grid:frame.Coordinate, isre:bool = True)->int:
        if tile_grid < self._size:
            if self._tileid_to_coo_list != None:
                if isre:
                    id_ans = int(self._coo_to_tileid_matrix[tile_grid.x(), tile_grid.y()])
                else:
                    id_ans = tile_grid.id(self._size.y())
            else:
                if isre:
                    id_ans = tile_grid.id(self._size.y())
                else:
                    raise TypeError(f"coo_to_tileid:error transfromation")   
        else:
            raise exception.CoordinateIndexError(f"Beyond the boundary of this tileset{self.name()}")
        return id_ans
    
    def coo_to_gid(self, tile_grid:frame.Coordinate, isre:bool = True)->int:
        return self.coo_to_tileid(tile_grid, isre = isre) + self.firstgid()
    
    def gid_to_coo(self, gid:int, isre:bool = True)->frame.TagCoordinate:
        return self.tileid_to_coo(self.gid_to_tileid(gid), isre = isre)

    def isexist(self)->bool:
        return self._properties.returnDefaultProperty("firstgid") != const.KEY.empty_tile
        



