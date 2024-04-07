# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et

import rwmap._util as utility
import rwmap._frame as frame

class TileSet(frame.ElementOri):
    def __init__(self, properties:frame.ElementProperties, column:int, image_properties:frame.ElementProperties = None,
                  png_text:str = None, tilelist_properties:list[frame.ElementProperties] = None)->None:
        super().__init__(properties)
        self._column = column
        self._image_properties = image_properties
        self._png_text = png_text
        self._tilelist_properties = tilelist_properties
    @classmethod
    def init_etElement(cls, root:et.Element, rwmaps_dir:str)->None:
        png_text_pro = utility.get_etElement_callable_from_tag(root, "properties")
        png_text = utility.get_etElement_name_to_text_rm(png_text_pro, "embedded_png")
        properties = frame.ElementProperties.init_etElement(root)
        image_properties = frame.ElementProperties.init_etElement(utility.get_etElement_callable_from_tag(root, "image"))
        tilelist_properties = [frame.ElementProperties.init_etElement(tile) for tile in root if tile.tag == "tile"]
        tilelist_properties = None if tilelist_properties == [] else tilelist_properties
        
        if properties.returnDefaultProperty("columns") == None:
            source_file = properties.returnDefaultProperty("source")

            source = rwmaps_dir + source_file
            root = et.ElementTree(file=source).getroot()
            if root.attrib.get("columns") == None:
                tilewidth = int(root.attrib["tilewidth"])
                image_element = utility.get_etElement_callable_from_tag(root, "image")
                if image_element.attrib.get("width") == None:
                    source_fa_dir = "/".join(source_file.split("/")[0:-1]) + "/"
                    source_fa_dir = "" if source_fa_dir == "/" else source_fa_dir
                    width = utility.image_width(rwmaps_dir + source_fa_dir + image_element.attrib["source"])
                else:
                    width = int(image_element.attrib["width"])
                column = int(width / tilewidth)
            else:
                column = int(root.attrib["columns"])

        else:
            column = int(properties.returnDefaultProperty("columns"))

        return cls(properties, column, image_properties, png_text, tilelist_properties)
    
    def output_str(self, pngtextnum:int = -1, tilenum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        if self._image_properties != None:
            str_ans = str_ans + self._image_properties.output_str() + "\n"
        if self._png_text != None:
            _png_text_now = self._png_text[:pngtextnum] if pngtextnum != -1 else ""
            str_ans = str_ans + _png_text_now + "\n"
        if self._tilelist_properties != None:
            str_ans = str_ans + "".join([self._tilelist_properties[i].output_str() + "\n" for i in range(0, tilenum)]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("tileset")
        self._properties.output_etElement(root)
        if self._image_properties != None:
            image_element = et.Element("image")
            self._image_properties.output_etElement(image_element)
            root.append(image_element)
        if self._png_text != None:
            png_element = et.Element("property", {"name": "embedded_png"})
            png_element.text = self._png_text
            properties = utility.get_etElement_callable_from_tag(root, "properties")
            properties.insert(0, png_element)
        if self._tilelist_properties != None:
            for tile in self._tilelist_properties:
                tile_element = et.Element("tile")
                tile.output_etElement(tile_element)
                root.append(tile_element)
        return root
    
    def output_name(self)->str:
        tileset_name = self._properties.returnDefaultProperty("name")
        if tileset_name == None:
            tileset_name = self._properties.returnDefaultProperty("source")
        tileset_name = utility.str_slash_to_dot(tileset_name)
        return tileset_name
    
    def tileid(self, tile_grid:frame.Coordinate)->int:
        id_now = tile_grid.id(self._column)
        id_ans = int(self._properties.returnDefaultProperty("firstgid")) + id_now
        return id_ans
        



