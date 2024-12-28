# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
from copy import deepcopy
import numpy as np
import os
import base64
from PIL import Image
import colorsys
import math
import networkx as nx
from itertools import product

import rwmap._util as utility
import rwmap._frame as frame
import rwmap._data.const as const
import rwmap._exceptions as exception
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties

def isinrange(data, range1, range2):
    return (data >= float(range1) and data <= float(range2)) ^ (float(range1) > float(range2))

def rgb_to_hsv(rgb:np.ndarray)->np.ndarray:
    return np.array(colorsys.rgb_to_hsv(float(rgb[0]) / 255, float(rgb[1]) / 255, float(rgb[2]) / 255))

def nparr_to_hex(nparr):
    if not isinstance(nparr, np.ndarray):
        raise ValueError("Input must be a NumPy array")

    if (nparr.shape != (3,) and nparr.shape != (4,))or nparr.dtype != np.uint8:
        raise ValueError(f"Input array must be of shape (3,)/(4,) and dtype uint8[{str(nparr.shape)}, {str(nparr.dtype)}]")

    hex_str = '#' + ''.join(f'{val:02x}' for val in nparr)

    return hex_str

def tilefunc_tileauto(tileprodictlist:list, rgb:np.ndarray)->str:

    hsv = rgb_to_hsv(rgb)
    for tilepro in tileprodictlist:
        if tilepro["type"] == "HSV":
            name = tilepro["name"]
            if tilepro.get("H-range") != None:
                if not isinrange(hsv[0], tilepro["H-range"][0], tilepro["H-range"][1]):
                    continue
            if tilepro.get("S-range") != None:
                if not isinrange(hsv[1], tilepro["S-range"][0], tilepro["S-range"][1]):
                    continue
            if tilepro.get("V-range") != None:
                if not isinrange(hsv[2], tilepro["V-range"][0], tilepro["V-range"][1]):
                    continue
            return name
    return None

wangset_id_list_1 = [
    ["0,2,0,1,0,2,0,2", "0,2,0,1,0,1,0,2", "0,2,0,2,0,1,0,2"], 
    ["0,1,0,1,0,2,0,2", "0,1,0,1,0,1,0,1", "0,2,0,2,0,1,0,1"], 
    ["0,1,0,2,0,2,0,2", "0,1,0,2,0,2,0,1", "0,2,0,2,0,2,0,1"]
]

terrain_list01 = [
    ["1,1,1,0", "1,1,0,0", "1,1,0,1"], 
    ["1,0,1,0", "0,0,0,0", "0,1,0,1"], 
    ["1,0,1,1", "0,0,1,1", "0,1,1,1"]
]

def listoflist_strmapc(listoflist:list[list[str]], mapdict:dict)->list[list[str]]:
    listoflist2 = []
    for i, list1 in enumerate(listoflist):
        listoflist2.append([])
        for ele in list1:
            listoflist2[i].append(utility.map_characters(ele, mapdict))
    return listoflist2

def tuple_strmapc(tuple1:tuple, mapdict:dict)->tuple:
    tuple2 = tuple([mapdict[ele] for ele in tuple1])
    return tuple2

wangset_id_list_2 = listoflist_strmapc(wangset_id_list_1, {'1': '2', '2': '1'})

class TileSet(ElementOri):
    pass

class TileSet(ElementOri):
    def __init__(self, properties:ElementProperties, size:frame.Coordinate, tile_size:frame.Coordinate, map_path:str, image_properties:ElementProperties = None,
                  png_text:str = None, tilelist_properties:list[ElementProperties] = [], coo_to_tileid_matrix:np.ndarray = None, 
                  tileid_to_coo_list:list[frame.Coordinate] = None, other_elements:list[et.Element] = [], isdependent_tsx = False)->None:
        super().__init__(const.TAG.tileset, properties)
        self._size = deepcopy(size)
        self._tile_size = deepcopy(tile_size)
        self._image_properties = deepcopy(image_properties)
        self._png_text = deepcopy(png_text)
        self._tilelist_properties = deepcopy(tilelist_properties)
        self._coo_to_tileid_matrix = deepcopy(coo_to_tileid_matrix)
        self._tileid_to_coo_list = deepcopy(tileid_to_coo_list)
        self._other_elements = deepcopy(other_elements)
        self._map_path = deepcopy(map_path)
        self._isdependent_tsx = isdependent_tsx
        self._tileid_to_treenode_index, self._terrain_tree = self.load_terrain()
        self._terrainid_to_tileid_dict = self.terrainid_to_tileid_dict()
        self._terrainname_to_terrainid_dict = self.terrainname_to_terrainid_dict()
    @classmethod
    def get_source_root(cls, map_path:str, rwmaps_dir:str, properties:ElementProperties)->et.Element:
        source_file_ori = properties.returnDefaultProperty("source")
        if source_file_ori == None or map_path == None:
            return None
        source_list = source_file_ori.split("/")
        source_list = source_list[utility.search_list_to_index(source_list, "maps") + 1:]
        source_list = source_list[utility.search_list_to_index(source_list, "tilesets") + 1:]
        source_file = "/".join(source_list)
        source = [rwmaps_dir + source_file, os.path.dirname(map_path) + '/' + source_file_ori]
        source_filenotfound = True
        for source_now in source:
            try:
                root = et.ElementTree(file = source_now).getroot()
            except FileNotFoundError:
                continue
            else:
                source_filenotfound = False
                break
        if source_filenotfound:
            raise FileNotFoundError(source)
        
        return root
    
    @classmethod
    def get_source_image(cls, map_path:str, rwmaps_dir:str, properties:ElementProperties)->et.Element:
        source_file_ori = properties.returnDefaultProperty("source")
        if source_file_ori == None or map_path == None:
            return None
        source_file = source_file_ori.split("/")[-1]
        source = [rwmaps_dir + "bitmaps/" + source_file, os.path.dirname(map_path) + '/' + source_file_ori]
        source_filenotfound = True
        for source_now in source:
            try:
                image = Image.open(source_now)
            except FileNotFoundError:
                continue
            else:
                source_filenotfound = False
                break
        if source_filenotfound:
            raise FileNotFoundError(source)
        
        return image

    @classmethod
    def init_etElement(cls, map_path:str, root:et.Element, rwmaps_dir:str, istilesort:bool = True)->TileSet:
        properties = ElementProperties.init_etElement(root)
        new_root = cls.dependent_tsx(map_path, rwmaps_dir, properties)
        if new_root != None:
            root_n = new_root
            if root.get('firstgid') != None:
                root_n.attrib['firstgid'] = root.attrib['firstgid']
            root_n.attrib['source'] = root.attrib['source']
            root_n.attrib.pop('tiledversion')
            root_n.attrib.pop('version')
            properties = ElementProperties.init_etElement(root_n)
            isdependent_tsx = True
        else:
            root_n = root
            isdependent_tsx = False
        png_text_pro = utility.get_etElement_callable_from_tag_s(root_n, "properties")
        png_text = utility.get_etElement_name_to_text_s(png_text_pro, "embedded_png")
        if png_text != None:
            properties.deleteOptionalProperty("embedded_png")
        image_properties = ElementProperties.init_etElement(utility.get_etElement_callable_from_tag_s(root_n, "image"))
        tilelist_properties = [ElementProperties.init_etElement(tile) for tile in root_n if tile.tag == "tile"]
        other_elements = utility.get_etElement_callable_from_tag_sup_s(root_n, "properties,image,tile")
        if istilesort:
            tilelist_properties.sort()

        if properties.returnDefaultProperty("columns") == None:
            
            tilewidth = int(root_n.attrib["tilewidth"])
            tileheight = int(root_n.attrib["tileheight"])

            if root_n.attrib.get("columns") == None:
                image_element = utility.get_etElement_callable_from_tag_s(root_n, "image")
                image_file = rwmaps_dir + "bitmaps/" + image_element.attrib["source"].split("/")[-1]
                width = utility.image_width(image_file)
                height = utility.image_height(image_file)

                column = int(width / tilewidth)
                row = int(height / tileheight)
            else:
                column = int(root_n.attrib["columns"])
                row = int(int(root_n.attrib["tilecount"]) / column)

        else:
            tilewidth = int(properties.returnDefaultProperty("tilewidth"))
            tileheight = int(properties.returnDefaultProperty("tileheight"))
            column = int(properties.returnDefaultProperty("columns"))
            row = int(int(properties.returnDefaultProperty("tilecount")) / column)

        size = frame.Coordinate(row, column)
        tile_size = frame.Coordinate(tileheight, tilewidth)

        coo_to_tileid_matrix = None
        tileid_to_coo_list = None
        
        if (not istilesort):
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

        tileset = cls(properties, size, tile_size, map_path, image_properties = image_properties, png_text = png_text, 
                      tilelist_properties = tilelist_properties, coo_to_tileid_matrix = coo_to_tileid_matrix, 
                      tileid_to_coo_list = tileid_to_coo_list, other_elements = other_elements, 
                      isdependent_tsx = isdependent_tsx)
        
        tileset.load_imageTile_list(rwmaps_dir, istilesort)
        return tileset
    
    @classmethod
    def init_pure_color(cls, rwmaps_dir:str, map_path:str, color_nparr:np.ndarray, tile_properties:list[list[str]], tile_size:frame.Coordinate, png_path:str, tsx_path:str, mode_code = 0, rand_seed = -1, limit_cycle = -1, isverbose = False, isdebug = False, noise:list[int] = [0, 0, 0], randseed:int = -1)->TileSet:

        real_nparr = utility.scale_nparr(color_nparr, tile_size)

        return cls.init_tilematrix(rwmaps_dir, map_path, real_nparr, tile_properties, tile_size, png_path, tsx_path, noise = noise, randseed = randseed)

    @classmethod
    def init_kmean(cls, tileset_size:frame.Coordinate, image_matrix:np.ndarray, rwmaps_dir:str, map_path:str, tile_size:frame.Coordinate, png_path:str, tsx_path:str, tile_properties_args = None, mode_code = 0, stopnum = 0, randseed = -1, limit_cycle = -1, isverbose = False, isdebug = False, noise:list[int] = [0, 0, 0])->TileSet:
        import rwmapautoc
        image_matrix = utility.memory_continuous_nparr(image_matrix)
        tileset_matrix:np.ndarray = rwmapautoc.tilesetauto(image_matrix, np.array([tileset_size.x(), tileset_size.y(), tile_size.x(), tile_size.y()], np.uint32), mode_code, stopnum, randseed, limit_cycle, isverbose, isdebug)

        tileset_matrix = tileset_matrix.reshape([tileset_size.x(), -1, tile_size.x(), tile_size.y(), 3])
        tile_properties_list = []
        
        if tile_properties_args != None:
            
            for i in range(tileset_matrix.shape[0]):
                tile_properties_list.append([])
                for j in range(tileset_matrix.shape[1]):
                    tile_pro = tilefunc_tileauto(tile_properties_args, tileset_matrix[i, j, 0, 0, :].reshape([3]))
                    tile_properties_list[i].append(tile_pro)

        tileset_matrix = tileset_matrix.transpose(0, 2, 1, 3, 4)
        tileset_matrix = tileset_matrix.reshape([tileset_size.x() * tile_size.x(), tileset_size.y() * tile_size.y(), 3])

        return cls.init_tilematrix(rwmaps_dir, map_path, tileset_matrix, tile_properties_list, tile_size, png_path, tsx_path, noise = noise, randseed = randseed)

    @classmethod
    def init_terrain(cls, name_list:list[str], color_list:list[np.ndarray], color_pair:list[tuple], delta_l:float, delta_x:float, delta_c:float, rwmaps_dir:str, map_path:str, tile_properties:list[str], tile_size:frame.Coordinate, png_path:str, tsx_path:str, noise:list[int] = [0, 0, 0], randseed:int = -1)->TileSet:
        # bezier_delta * bezier_k < 1\
        tx = tile_size.x()
        ty = tile_size.y()

        ix = 7
        iy = max(len(color_pair) * 3, len(color_list))

        tilematrix = np.ndarray([ix * tx, iy * ty, 4], np.uint8)

        tilematrix = np.zeros(tilematrix.shape, np.uint8)

        color_list_new = color_list.copy()
        for color_i, color in enumerate(color_list_new):
            color_list_new[color_i] = np.append(color, 255) if color.shape[0] == 3 else color
        tile_properties_n = [[], [], [], [], [], [], []]
        for tile_i, color in enumerate(color_list_new):
            if tile_i < len(tile_properties):
                tile_properties_n[0].append(tile_properties[tile_i])
            tilematrix[0:tx, tile_i * ty: (tile_i + 1) * ty, :color.shape[0]] = utility.scale_nparr(color.reshape([1, 1, -1]).astype(np.uint8), tile_size)
        
        wangsets = et.Element('wangsets')

        for tile_i, color_index_t in enumerate(color_pair):

            wangset = et.Element('wangset', {'name': name_list[color_index_t[0]] + '-' + name_list[color_index_t[1]], 
                                              'type': "corner", "tile": "-1"})

            color1 = color_list_new[color_index_t[0]]
            color2 = color_list_new[color_index_t[1]]

            wangcolor1 = et.Element('wangcolor', {'name': name_list[color_index_t[0]], 
                                              'color': nparr_to_hex(color_list[color_index_t[0]]), "tile": "-1", "probability": "1"})
            wangcolor2 = et.Element('wangcolor', {'name': name_list[color_index_t[1]], 
                                              'color': nparr_to_hex(color_list[color_index_t[1]]), "tile": "-1", "probability": "1"})
            wangset.append(wangcolor1)
            wangset.append(wangcolor2)
            wangtile1 = et.Element('wangtile', {'tileid': str(color_index_t[0]), "wangid": wangset_id_list_1[1][1]})
            wangtile2 = et.Element('wangtile', {'tileid': str(color_index_t[1]), "wangid": wangset_id_list_2[1][1]})
            wangset.append(wangtile1)
            wangset.append(wangtile2)

            for wi in range(3):
                for wj in range(3):
                    if wi == 1 and wj == 1:
                        continue
                    tileid1 = (wi + 1) * iy + wj + (3 * tile_i)
                    tileid2 = (wi + 4) * iy + wj + (3 * tile_i)
                    wangtile1 = et.Element('wangtile', {'tileid': str(tileid1), "wangid": wangset_id_list_1[wi][wj]})
                    wangtile2 = et.Element('wangtile', {'tileid': str(tileid2), "wangid": wangset_id_list_2[wi][wj]})
                    wangset.append(wangtile1)
                    wangset.append(wangtile2)


            narr_l12 = utility.scale_nparr_l(color1, color2, delta_l, delta_x, delta_c, tile_size)
            narr_l21 = utility.scale_nparr_l(color2, color1, delta_l, delta_x, delta_c, tile_size)
            narr_lt12 = utility.scale_nparr_lt(color1, color2, delta_l, delta_x, delta_c, tile_size)
            narr_lt21 = utility.scale_nparr_lt(color2, color1, delta_l, delta_x, delta_c, tile_size)

            if color_index_t[1] < len(tile_properties):
                tile_properties_n[1].append(tile_properties[color_index_t[1]])
                tile_properties_n[1].append(tile_properties[color_index_t[1]])
                tile_properties_n[1].append(tile_properties[color_index_t[1]])
                tile_properties_n[2].append(tile_properties[color_index_t[1]])
                tile_properties_n[2].append(None)
                tile_properties_n[2].append(tile_properties[color_index_t[1]])
                tile_properties_n[3].append(tile_properties[color_index_t[1]])
                tile_properties_n[3].append(tile_properties[color_index_t[1]])
                tile_properties_n[3].append(tile_properties[color_index_t[1]])
            if color_index_t[0] < len(tile_properties):
                tile_properties_n[4].append(tile_properties[color_index_t[0]])
                tile_properties_n[4].append(tile_properties[color_index_t[0]])
                tile_properties_n[4].append(tile_properties[color_index_t[0]])
                tile_properties_n[5].append(tile_properties[color_index_t[0]])
                tile_properties_n[5].append(None)
                tile_properties_n[5].append(tile_properties[color_index_t[0]])
                tile_properties_n[6].append(tile_properties[color_index_t[0]])
                tile_properties_n[6].append(tile_properties[color_index_t[0]])
                tile_properties_n[6].append(tile_properties[color_index_t[0]])



            tilematrix_now12 = np.ndarray([3 * tx, 3 * ty, 4], np.uint8)
            tilematrix_now12 = np.zeros(tilematrix_now12.shape, np.uint8)

            tilematrix_now12[0:tx, 0:ty] = np.flip(narr_lt12, (0, 1))
            tilematrix_now12[0:tx, ty * 2:ty * 3] = np.flip(narr_lt12, (0))
            tilematrix_now12[tx * 2:tx * 3, 0:ty] = np.flip(narr_lt12, (1))
            tilematrix_now12[tx * 2:tx * 3, ty * 2:ty * 3] = narr_lt12

            tilematrix_now12[0:tx, ty:ty * 2] = np.flip(narr_l12.transpose((1, 0, 2)), (0))
            tilematrix_now12[tx:tx * 2, 0:ty] = np.flip(narr_l12, (1))
            tilematrix_now12[tx:tx * 2, ty * 2:ty * 3] = narr_l12
            tilematrix_now12[tx * 2:tx * 3, ty:ty * 2] = narr_l12.transpose((1, 0, 2))

            tilematrix[tx:tx * 4, ty * tile_i * 3: ty * (tile_i + 1) * 3] = tilematrix_now12


            tilematrix_now21 = np.ndarray([3 * tx, 3 * ty, 4], np.uint8)
            tilematrix_now21 = np.zeros(tilematrix_now21.shape, np.uint8)

            tilematrix_now21[0:tx, 0:ty] = np.flip(narr_lt21, (0, 1))
            tilematrix_now21[0:tx, ty * 2:ty * 3] = np.flip(narr_lt21, (0))
            tilematrix_now21[tx * 2:tx * 3, 0:ty] = np.flip(narr_lt21, (1))
            tilematrix_now21[tx * 2:tx * 3, ty * 2:ty * 3] = narr_lt21

            tilematrix_now21[0:tx, ty:ty * 2] = np.flip(narr_l21.transpose((1, 0, 2)), (0))
            tilematrix_now21[tx:tx * 2, 0:ty] = np.flip(narr_l21, (1))
            tilematrix_now21[tx:tx * 2, ty * 2:ty * 3] = narr_l21
            tilematrix_now21[tx * 2:tx * 3, ty:ty * 2] = narr_l21.transpose((1, 0, 2))

            tilematrix[tx * 4:tx * 7, ty * tile_i * 3: ty * (tile_i + 1) * 3] = tilematrix_now21

            wangsets.append(wangset)

        return cls.init_tilematrix(rwmaps_dir, map_path, tilematrix, tile_properties_n, tile_size, png_path, tsx_path, noise = noise, randseed = randseed, other_elements = [wangsets])

    @classmethod
    def init_terrain_nt_t(cls, name_list:list[str], color_list:list[np.ndarray], color_pair:list[list], delta_lxc:list[list[float]], rwmaps_dir:str, map_path:str, tile_properties:list[str], tile_size:frame.Coordinate, png_path:str, tsx_path:str, tiy:int = -1, noise:list[list[float]] = [], randseed:int = -1, terrain_index_dict:dict = {})->TileSet:
        # 0 =< delta <= 1

        oth_properties = {"forced_autotile": "", "layer": "ground"}

        tx = tile_size.x()
        ty = tile_size.y()

        tiy = tiy if tiy != -1 else len(color_pair)
        tix = math.ceil(len(color_pair) / tiy)

        iy = tiy * 3
        ix = tix * 6

        tilematrix = np.zeros((ix * tx, iy * ty, 4), np.uint8)

        
        terraintypes = et.Element('terraintypes')

        color_list_new = color_list.copy()
        for color_i, color in enumerate(color_list_new):
            color_list_new[color_i] = np.append(color, 255) if color.shape[0] == 3 else color

        tile_coo_dict = {}
        tileid_dict = {}
        tile_noised_dict = {}

        terrain_exist_set = set()
        for cij_s, tile_i in terrain_index_dict.items():
            terrain_exist_set.add(tile_i)

        for tile_i, color_index_t in enumerate(color_pair):
            tile_ix = tile_i // tiy
            tile_iy = tile_i % tiy
            for tile_j, cij in enumerate(color_index_t):
                if tile_coo_dict.get(cij) == None and terrain_index_dict.get(str(cij)) == tile_i:
                    color = color_list_new[cij]
                    tile_scale = utility.scale_nparr(color.reshape([1, 1, -1]).astype(np.uint8), tile_size)
                    if cij < len(noise):
                        tile_noised_dict[cij] = utility.add_hsv_gaussian_noise(tile_scale, noise[cij], randseed = randseed)
                    tile_coo_dict[cij] = frame.Coordinate(tile_i, tile_j)
                    tileid = ((6 * tile_ix + 3 * tile_j + 1) * iy + 3 * tile_iy + 1)
                    tileid_dict[cij] = tileid
        
        for cij_s, tile_i in terrain_index_dict.items():
            cij = int(cij_s)
            tile_ix = tile_i // tiy
            tile_iy = tile_i % tiy
            tile_j = color_pair[tile_i].index(cij)
            tileid = ((6 * tile_ix + 3 * tile_j + 1) * iy + 3 * tile_iy + 1)
            if tileid_dict.get(cij) != None:
                terrain = et.Element('terrain', {'name': name_list[cij], 'tile': str(tileid_dict[cij])})
                terraintypes.append(terrain)

        for tile_i in range(len(color_list_new)):
            if tile_coo_dict.get(tile_i) == None:
                raise KeyError("color_pair can't cover all color.")

        tile_properties_n = []
        terrain_properties_n = []
        for tile_i in range(ix):
            tile_properties_n.append([])
            terrain_properties_n.append([])

        wangsets = et.Element('wangsets')

        for tile_i, color_index_t in enumerate(color_pair):
            tile_ix = tile_i // tiy
            tile_iy = tile_i % tiy
            cijt = color_index_t[0] if delta_lxc[tile_i][0] > 0.5 else color_index_t[1]
            for tile_j, cij in enumerate(color_index_t):
                tile_j_o = (tile_j + 1) % 2
                cij_o = color_index_t[tile_j_o]
                noise_n = noise[cij] if cij < len(noise) else np.zeros(())
                noise_o = noise[cij_o]
                str_end = "(*)" if not tile_i in terrain_exist_set else ""
                wangset = et.Element('wangset', {'name': name_list[cij] + '-' + name_list[cij_o] + str_end, 
                                              'type': "corner", "tile": "-1"})
                color = color_list_new[cij]
                color_o = color_list_new[cij_o]

                wangcolor = et.Element('wangcolor', {'name': name_list[cij], 
                                                'color': nparr_to_hex(color_list[cij]), "tile": "-1", "probability": "1"})
                wangcolor_o = et.Element('wangcolor', {'name': name_list[cij_o], 
                                                'color': nparr_to_hex(color_list[cij_o]), "tile": "-1", "probability": "1"})
                wangset.append(wangcolor)
                wangset.append(wangcolor_o)

                wangtile1 = et.Element('wangtile', {'tileid': str(tileid_dict[cij]), "wangid": wangset_id_list_1[1][1]})
                wangtile2 = et.Element('wangtile', {'tileid': str(tileid_dict[cij_o]), "wangid": wangset_id_list_2[1][1]})
                
                wangset.append(wangtile1)
                wangset.append(wangtile2)

                if tile_i in terrain_exist_set:
                    terrain_tmatrix = listoflist_strmapc(terrain_list01, {'0': str(cij), '1':str(cij_o)})

                    tcoo = tile_coo_dict.get(cij)
                    for wi in range(3):
                        for wj in range(3):
                            
                            if ((wi + wj) % 2 == 1 and tile_j == 1) or (wi == 1 and wj == 1 and (tcoo.x() != tile_i or tcoo.y() != tile_j)):
                                terrain_properties_n[6 * tile_ix + 3 * tile_j + wi].append(None)
                            else:
                                terrain_properties_n[6 * tile_ix + 3 * tile_j + wi].append(terrain_tmatrix[wi][wj])

                else:
                    for wi in range(3):
                        for wj in range(3):
                            terrain_properties_n[6 * tile_ix + 3 * tile_j + wi].append(None)


                for wi in range(3):
                    for wj in range(3):
                        if wi == 1 and wj == 1:
                            tile_properties_n[6 * tile_ix + 3 * tile_j + wi].append(utility.list_get_s(tile_properties, cij))
                            continue
                        if (wi + wj) % 2 == 1:
                            tile_properties_n[6 * tile_ix + 3 * tile_j + wi].append(utility.list_get_s(tile_properties, cijt))
                        else:
                            tile_properties_n[6 * tile_ix + 3 * tile_j + wi].append(utility.list_get_s(tile_properties, cij_o))

                        tileid = (6 * tile_ix + 3 * tile_j + wi) * iy + wj + (3 * tile_iy)
                        wangtile = et.Element('wangtile', {'tileid': str(tileid), "wangid": wangset_id_list_1[wi][wj]})
                        
                        
                        wangset.append(wangtile)

                for wi in range(3):
                    for wj in range(3):
                        if (wi + wj) % 2 == 1 or (wi == 1 and wj == 1):
                            continue
                        tileid = (6 * tile_ix + 3 * tile_j_o + wi) * iy + wj + (3 * tile_iy)
                        wangtile = et.Element('wangtile', {'tileid': str(tileid), "wangid": wangset_id_list_2[wi][wj]})
                        
                        wangset.append(wangtile)

                tilematrix_now = np.zeros((3 * tx, 3 * ty, 4), np.uint8)
                
                delta_l_n = delta_lxc[tile_i][0] if tile_j == 0 else 1 - delta_lxc[tile_i][0]
                delta_x_n = delta_lxc[tile_i][1]
                delta_c_n = delta_lxc[tile_i][2]

                if tile_j == 0:
                    narr_l = utility.scale_nparr_l(color, color_o, noise_n, noise_o, delta_l_n, delta_x_n, delta_c_n, tile_size)
                else:
                    narr_l = np.flip(narr_l, axis = 1)
                narr_lt = utility.scale_nparr_lt(color, color_o, noise_n, noise_o, delta_l_n, delta_x_n, delta_c_n, tile_size)
                

                tilematrix_now[tx:tx * 2, ty:ty * 2] = tile_noised_dict[cij]

                tilematrix_now[0:tx, 0:ty] = np.flip(narr_lt, (0, 1))
                tilematrix_now[0:tx, ty * 2:ty * 3] = np.flip(narr_lt, (0))
                tilematrix_now[tx * 2:tx * 3, 0:ty] = np.flip(narr_lt, (1))
                tilematrix_now[tx * 2:tx * 3, ty * 2:ty * 3] = narr_lt

                tilematrix_now[0:tx, ty:ty * 2] = np.flip(narr_l.transpose((1, 0, 2)), (0))
                tilematrix_now[tx:tx * 2, 0:ty] = np.flip(narr_l, (1))
                tilematrix_now[tx:tx * 2, ty * 2:ty * 3] = narr_l
                tilematrix_now[tx * 2:tx * 3, ty:ty * 2] = narr_l.transpose((1, 0, 2))

                tilematrix[(tile_ix * 2 + tile_j) * tx * 3:(tile_ix * 2 + tile_j + 1) * tx * 3, tile_iy * ty * 3: (tile_iy + 1) * ty * 3] = tilematrix_now
                if tile_j == 0:
                    wangsets.append(wangset)

        return cls.init_tilematrix(rwmaps_dir, map_path, tilematrix, tile_properties_n, tile_size, png_path, tsx_path, randseed = randseed, other_elements = [wangsets, terraintypes], terrain_properties = terrain_properties_n, oth_properties = oth_properties)
    
    @classmethod
    def init_tilematrix(cls, rwmaps_dir:str, map_path:str, tilematrix:np.ndarray, tile_properties:list[list[str]], tile_size:frame.Coordinate, png_path:str, tsx_path:str, noise:list[int] = [0, 0, 0], randseed:int = -1, other_elements:list = [], terrain_properties:list[list[str]] = [], oth_properties = {})->TileSet:
        

        tilematrix_n = utility.add_hsv_gaussian_noise(tilematrix, noise, randseed = randseed) if noise != [0, 0, 0] else tilematrix.copy()
        
        tsx_real_path = utility.combine_path(os.path.dirname(map_path), tsx_path)
        png_real_path = utility.combine_path(os.path.dirname(tsx_real_path), png_path)

        utility.write_file_fromndarray(png_real_path, tilematrix_n)
        size = (tilematrix.shape / np.array(tile_size.x(), tile_size.y())).astype(np.int32)
        tilecount = size[0] * size[1]
        columns = size[1]
        properties = ElementProperties("tileset", 
                                       {'version':"1.10", 'tiledversion':"1.10.2", 
                                        'name': os.path.basename(png_path).split('.')[0], 
                                        'tilewidth': str(tile_size.y()), 'tileheight': str(tile_size.x()), 
                                        'tilecount': str(tilecount), 'columns': str(columns)}, oth_properties)
        
        image_properties = ElementProperties("image", 
                                             {'source': os.path.basename(png_path), 
                                              'width': str(size[1]), 'height': str(size[0])})
        tsx_element = et.Element('tileset')
        tsx_element = properties.output_etElement(tsx_element)
        image_element = et.Element('image')
        image_element = image_properties.output_etElement(image_element)
        for index_x in range(tilematrix.shape[0]):
            for index_y in range(tilematrix.shape[1]):
                
                isdo = False
                oep = {'id': str(index_y + index_x * columns)}
                if index_x < len(terrain_properties) and index_y < len(terrain_properties[index_x]) and terrain_properties[index_x][index_y] != None:
                    oep['terrain'] = str(terrain_properties[index_x][index_y])
                    isdo = True

                othep = {}
                if index_x < len(tile_properties) and index_y < len(tile_properties[index_x]) and tile_properties[index_x][index_y] != None:
                    othep[tile_properties[index_x][index_y]] = ''
                    isdo = True
                
                if isdo:
                    tile_elepro = ElementProperties("tile", oep, othep)
                    tile_ele = et.Element('tile')
                    tile_ele = tile_elepro.output_etElement(tile_ele)
                    tsx_element.append(tile_ele)

        for other_ele in other_elements:
            tsx_element.append(other_ele)

        tsx_element.append(image_element)

        utility.output_file_from_etElement(tsx_element, tsx_real_path)

        tileset_properties = ElementProperties("tileset", 
                                               {"source": tsx_path})

        tileset_ele = tileset_properties.output_etElement(et.Element("tileset"))

        tileSet = cls.init_etElement(map_path, tileset_ele, rwmaps_dir)

        return tileSet

    def size(self)->frame.Coordinate:
        return self._size
    
    def tile_size(self)->frame.Coordinate:
        return self._tile_size

    @classmethod
    def dependent_tsx(cls, map_path:str, rwmaps_dir:str, properties:ElementProperties)->et.Element:
        tileset_root = TileSet.get_source_root(map_path, rwmaps_dir, properties)
        if tileset_root == None:
            return None
        return tileset_root

    def dependent_png(self, rwmaps_dir:str)->TileSet:
        if self._png_text != None:
            return self
        tileset_png = TileSet.get_source_image(self._map_path, rwmaps_dir, self._image_properties)
        tileset_now = deepcopy(self)
        if tileset_png != None:
            tileset_now._png_text = utility.get_png_text(tileset_png)
        else:
            raise ValueError("png_text cannot find.")
        return tileset_now

    def dependent(self, rwmaps_dir:str)->TileSet:
        tileset_now = self.dependent_png(rwmaps_dir)
        tileset_now._isdependent_tsx = False
        return tileset_now

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

    def output_etElement(self, isdeletetsxsource:bool = False, isdeleteimgsource:bool = False)->et.Element:
        root = et.Element("tileset")
        if self._isdependent_tsx:
            root.attrib['firstgid'] = self._properties.returnDefaultProperty('firstgid')
            root.attrib['source'] = self._properties.returnDefaultProperty('source')
        else:
            temp_pro = deepcopy(self._properties)
            if isdeletetsxsource:
                temp_pro.deleteDefaultProperty('source')
            root = temp_pro.output_etElement(root)
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
                if isdeleteimgsource and self._png_text != None and self._image_properties.returnDefaultProperty("source") != None:
                    self._image_properties.deleteDefaultProperty("source")
                image_element = self._image_properties.output_etElement(image_element)
                root.append(image_element)
            if self._tilelist_properties != []:
                for tile in self._tilelist_properties:
                    tile_element = et.Element("tile")
                    tile_element = tile.output_etElement(tile_element)
                    root.append(tile_element)
            if self._other_elements != []:
                other_elements = self._other_elements
                for one_element in other_elements:
                    root.append(one_element)
        return root
    
    def write_png(self, dir:str)->None:
        if self._image_properties != None:
            if self._png_text == None:
                return None
            pngbyte = base64.b64decode(self._png_text.encode('utf-8'))
            file_path = dir + '/' + self._image_properties.returnDefaultProperty("source")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as file_now:
                file_now.write(pngbyte)

    def change_map_path(self, map_path:str)->None:
        if self._image_properties != None:
            im_source = self._image_properties.returnDefaultProperty('source')
            if im_source != None:
                self._image_properties.assignDefaultProperty('source', utility.get_path(map_path, self._map_path, im_source))
        tsx_source = self._properties.returnDefaultProperty('source')
        if tsx_source != None:
            self._properties.assignDefaultProperty('source', utility.get_path(map_path, self._map_path, tsx_source))
        self._map_path = map_path

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

    def exist_gid_to_tileid(self, gid:int)->bool:
        return gid >= self.firstgid() and gid < self.endgid()

    def gid_to_tileid(self, gid:int)->tuple[str, int]:
        tileid = gid - self.firstgid()
        if tileid < 0 or tileid >= self.totalgid():
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

    def contain(self, tile_grid:frame.Coordinate)->bool:
        return tile_grid < self._size and tile_grid > const.COO.SIZE_ZERO

    def coo_to_tileid(self, tile_grid:frame.Coordinate, isre:bool = True)->int:
        if self.contain(tile_grid):
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
    
    def rec_to_tileid(self, tile_rec_grid:frame.Rectangle, isre:bool = True)->set[int]:
        tileidset = set()
        tile_rec_grid_temp = tile_rec_grid + frame.Coordinate(1, 1)
        for tile_grid in tile_rec_grid_temp:
            tileid = self.coo_to_tileid(tile_grid, isre = isre)
            tileidset.add(tileid)
        return tileidset
    
    def rec_to_gid(self, tile_rec_grid:frame.Rectangle, isre:bool = True)->set[int]:
        return {x + self.firstgid() for x in self.rec_to_tileid(tile_rec_grid, isre = isre)}

    def gid_to_coo(self, gid:int, isre:bool = True)->frame.TagCoordinate:
        return self.tileid_to_coo(self.gid_to_tileid(gid), isre = isre)

    def isexist(self)->bool:
        try:
            return self._properties.returnDefaultProperty("firstgid") != const.KEY.empty_tile
        except:
            import pdb;pdb.set_trace()

    def get_png_text(self, rwmaps_dir:str, istilesort:bool = True)->str:
        tileset_now = self.dependent_png(rwmaps_dir)
        return tileset_now._png_text

    def load_imageTile_list(self, rwmaps_dir:str, istilesort:bool = True)->tuple[list[np.ndarray], int]:
        png_text = self.get_png_text(rwmaps_dir, istilesort = istilesort)
        if png_text == None:
            import pdb
            pdb.set_trace()
        image = utility.get_image_from_png_text(png_text)
        image_list, columns = utility.image_division(image, self.tile_size())
        self._imageTile_list = image_list
        return image_list, columns
        
    def imageTile_fromTileid(self, tileid:int)->np.ndarray:
        return self._imageTile_list[tileid]
    
    def load_terrain(self)->tuple[dict, nx.Graph]:
        tileid_to_treenode_index = {}
        terrain_tree = nx.Graph()
        terrain_set = set()
        terrain_edge_set = set()
        for tile_pro in self._tilelist_properties:
            tileid = int(tile_pro.returnDefaultProperty("id"))
            tile_terrain = tile_pro.returnDefaultProperty("terrain")
            if tile_terrain == None:
                continue
            tile_terrain_list = [int(st) for st in tile_terrain.split(",")]
            tile_terrain_set = set()
            for terrain in tile_terrain_list:
                if not terrain in terrain_set:
                    terrain_set.add(terrain)
                    terrain_tree.add_node(terrain, data = [])
                tile_terrain_set.add(terrain)

            tile_terrain_stuple = tuple(tile_terrain_set)

            if len(tile_terrain_set) == 2:

                if tile_terrain_stuple[0] > tile_terrain_stuple[1]:
                    tile_terrain_stuple = (tile_terrain_stuple[1], tile_terrain_stuple[0])

                if not tile_terrain_stuple in terrain_edge_set:
                    terrain_edge_set.add(tile_terrain_stuple)
                    terrain_index = tuple([tile_terrain_stuple.index(terrain) for terrain in tile_terrain_list])
                    
                    terrain_nparr = np.ndarray((2, 2, 2, 2), dtype = object)
                    for i in product((0, 1), repeat = 4):
                        terrain_nparr[i] = []

                    terrain_nparr[terrain_index].append(tileid)
                    terrain_tree.add_edge(tile_terrain_stuple[0], tile_terrain_stuple[1], data = terrain_nparr)

                else:
                    terrain_index = tuple([tile_terrain_stuple.index(terrain) for terrain in tile_terrain_list])
                    terrain_tree[tile_terrain_stuple[0]][tile_terrain_stuple[1]]['data'][terrain_index].append(tileid)

                tileid_to_treenode_index[tileid] = [tile_terrain_stuple, terrain_index]

            else:
                terrain_tree.nodes[tile_terrain_stuple[0]]['data'].append(tileid)
                tileid_to_treenode_index[tileid] = [tile_terrain_stuple[0]]

        return (tileid_to_treenode_index, terrain_tree)

    def tileid_to_terrain(self, tileid:int)->tuple[int]:
        terrain_now = self._tileid_to_treenode_index.get(tileid)
        if terrain_now == None:
            import pdb;pdb.set_trace()
            raise ValueError("TileSet: tileid_to_terrain(tileid cannot match a terrain)")
        if len(terrain_now) == 1:
            return tuple([terrain_now[0] for i in range(4)])
        else:
            return tuple_strmapc(terrain_now[1], {0: terrain_now[0][0], 1: terrain_now[0][1]})
        
    def terrain_expand(self, terrain:tuple[int])->tuple[tuple[tuple[int]]]:
        return (
            ((-1, -1, -1, terrain[0]), (-1, -1, terrain[0], terrain[1]), (-1, -1, terrain[1], -1)), 
            ((-1, terrain[0], -1, terrain[2]), terrain, (terrain[1], -1, terrain[3], -1)), 
            ((-1, terrain[2], -1, -1), (terrain[2], terrain[3], -1, -1), (terrain[3], -1, -1, -1))
        )
    
    def tileid_to_terrain_expand(self, tileid:int)->tuple[tuple[tuple[int]]]:
        terrain = self.tileid_to_terrain(tileid)
        return self.terrain_expand(terrain)

    def terrain_to_tileid(self, terrain_now:tuple[int])->int:
        terrain_now_set = set(terrain_now)
        if len(terrain_now_set) > 2 or len(terrain_now_set) < 1:
            raise ValueError("TileSet: terrain_to_tileid(The kind terrain are more than 2 or empty)")
        elif len(terrain_now_set) == 1:
            tileid_l = self._terrain_tree.nodes[terrain_now[0]]['data']
        else:
            terrain_now_tuple = tuple(terrain_now_set)
            if terrain_now_tuple[0] > terrain_now_tuple[1]:
                terrain_now_tuple = (terrain_now_tuple[1], terrain_now_tuple[0])
            terrain_index = tuple_strmapc(terrain_now, {terrain_now_tuple[0]:0, terrain_now_tuple[1]:1})
            tileid_l = self._terrain_tree[terrain_now_tuple[0]][terrain_now_tuple[1]]['data'][terrain_index]
        
        if len(tileid_l) == 0:
            raise ValueError("TileSet: terrain_to_tileid(terrain cannot match a tileid)")
        else:
            return tileid_l[0]

    def terrain_to_gid(self, terrainid:int)->int:
        return self.tileid_to_gid(self.terrain_to_tileid(terrainid))

    def terrainid_to_tileid(self, terrainid:int)->int:
        return self.terrain_to_tileid(tuple([terrainid for i in range(4)]))
    
    def terrainid_to_gid(self, terrainid:int)->int:
        return self.tileid_to_gid(self.terrain_to_tileid(terrainid))

    def terrain_trans_to_tileid(self, tileid:int, terrain_index_tuple:tuple[int])->int:
        terrain_now = list(self.tileid_to_terrain(tileid))
        for index, terrain_i in enumerate(terrain_index_tuple):
            if terrain_i >= 0:
                terrain_now[index] = terrain_i
        return self.terrain_to_tileid(tuple(terrain_now))

    def terrainname_to_terrainid_dict(self)->dict[str, int]:
        terrainname_to_terrainid_dict_now = {}
        for terrain_l in self._other_elements:
            if terrain_l.tag == "terraintypes":
                for i, terrain_e in enumerate(terrain_l):
                    terrainname_to_terrainid_dict_now[terrain_e.attrib["name"]] = i
        return terrainname_to_terrainid_dict_now
    
    def terrainname_to_terrainid(self, terrainname:str)->int:
        return self._terrainname_to_terrainid_dict[terrainname]

    def terrainid_to_tileid_dict(self)->dict[int, int]:
        terrainid_to_tileid_dict_now = {}
        for terrain_l in self._other_elements:
            if terrain_l.tag == "terraintypes":
                for i, terrain_e in enumerate(terrain_l):
                    terrainid_to_tileid_dict_now[i] = int(terrain_e.attrib["tile"])
        return terrainid_to_tileid_dict_now

