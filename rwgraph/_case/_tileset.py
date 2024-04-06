# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et

import rwgraph._util as utility

class TileSet:
    def __init__(self, tileset_properties:utility.ElementProperties, image_properties:utility.ElementProperties = None,
                  png_text:str = None, tilelist_properties:list[utility.ElementProperties] = None)->None:
        self.tileset_properties = tileset_properties
        self.image_properties = image_properties
        self.png_text = png_text
        self.tilelist_properties = tilelist_properties
    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        png_text_pro = utility._get_etElement_callable_from_tag(root, "properties")
        png_text = utility._get_etElement_name_to_text_rm(png_text_pro, "embedded_png")
        tileset_properties = utility.ElementProperties.init_etElement(root)
        image_properties = utility.ElementProperties.init_etElement(utility._get_etElement_callable_from_tag(root, "image"))
        tilelist_properties = [utility.ElementProperties.init_etElement(tile) for tile in root if tile.tag == "tile"]
        tilelist_properties = None if tilelist_properties == [] else tilelist_properties
        return cls(tileset_properties, image_properties, png_text, tilelist_properties)
    
    def output_str(self, pngtextnum:int = -1, tilenum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self.tileset_properties.output_str() + "\n"
        if self.image_properties != None:
            str_ans = str_ans + self.image_properties.output_str() + "\n"
        if self.png_text != None:
            png_text_now = self.png_text[:pngtextnum] if pngtextnum != -1 else ""
            str_ans = str_ans + png_text_now + "\n"
        if self.tilelist_properties != None:
            str_ans = str_ans + "".join([self.tilelist_properties[i].output_str() + "\n" for i in range(0, tilenum)]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("tileset")
        self.tileset_properties.output_etElement(root)
        if self.image_properties != None:
            image_element = et.Element("image")
            self.image_properties.output_etElement(image_element)
            root.append(image_element)
        if self.png_text != None:
            png_element = et.Element("property", {"name": "embedded_png"})
            png_element.text = self.png_text
            properties = utility._get_etElement_callable_from_tag(root, "properties")
            properties.insert(0, png_element)
        if self.tilelist_properties != None:
            for tile in self.tilelist_properties:
                tile_element = et.Element("tile")
                tile.output_etElement(tile_element)
                root.append(tile_element)
        return root



