# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
from copy import deepcopy

import rwmap._util as utility
import rwmap._frame as frame
import rwmap._exceptions as exception
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties

class TileSet(ElementOri):
    def __init__(self, properties:ElementProperties, size:frame.Coordinate, image_properties:ElementProperties = None,
                  png_text:str = None, tilelist_properties:list[ElementProperties] = None)->None:
        super().__init__(properties)
        self._size = deepcopy(size)
        self._image_properties = deepcopy(image_properties)
        self._png_text = deepcopy(png_text)
        self._tilelist_properties = deepcopy(tilelist_properties)
    @classmethod
    def init_etElement(cls, root:et.Element, rwmaps_dir:str)->None:
        png_text_pro = utility.get_etElement_callable_from_tag_s(root, "properties")
        png_text = utility.get_etElement_name_to_text_s(png_text_pro, "embedded_png")
        properties = ElementProperties.init_etElement(root)
        if png_text != None:
            properties.deleteOptionalProperty("embedded_png")
        image_properties = ElementProperties.init_etElement(utility.get_etElement_callable_from_tag_s(root, "image"))
        tilelist_properties = [ElementProperties.init_etElement(tile) for tile in root if tile.tag == "tile"]
        tilelist_properties = None if tilelist_properties == [] else tilelist_properties
        
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
        return cls(properties, size, image_properties, png_text, tilelist_properties)
    
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
        if self._image_properties != None:
            image_element = et.Element("image")
            image_element = self._image_properties.output_etElement(image_element)
            root.append(image_element)
        if self._png_text != None:
            png_element = et.Element("property", {"name": "embedded_png"})
            png_element.text = self._png_text
            properties = utility.get_etElement_callable_from_tag_s(root, "properties")
            properties.insert(0, png_element)
        if self._tilelist_properties != None:
            for tile in self._tilelist_properties:
                tile_element = et.Element("tile")
                tile_element = tile.output_etElement(tile_element)
                root.append(tile_element)
        return root
    
    def name(self)->str:
        tileset_name = self._properties.returnDefaultProperty("name")
        if tileset_name == None:
            tileset_name = self._properties.returnDefaultProperty("source")
        tileset_name = utility.str_slash_to_dot(tileset_name)
        return tileset_name
    
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
    
    def tileid_to_coo(self, tileid:int)->frame.TagCoordinate:
        if tileid < self.totalgid:
            tagcoo = frame.TagCoordinate.init_id(self.name(), tileid, self._size.y())
        else:
            raise exception.CoordinateIndexError(f"Beyond the boundary of this tileset{self.name()}")
        return tagcoo

    def coo_to_tileid(self, tile_grid:frame.Coordinate)->int:
        if tile_grid < self._size:
            id_ans = tile_grid.id(self._size.y())
        else:
            raise exception.CoordinateIndexError(f"Beyond the boundary of this tileset{self.name()}")
        return id_ans
    
    def coo_to_gid(self, tile_grid:frame.Coordinate)->int:
        return self.coo_to_tileid(tile_grid) + self.firstgid()
    
    def gid_to_coo(self, gid:int)->frame.TagCoordinate:
        return self.tileid_to_coo(self.gid_to_tileid(gid))

    def isexist(self)->bool:
        return self._properties.returnDefaultProperty("firstgid") != "0"
        



