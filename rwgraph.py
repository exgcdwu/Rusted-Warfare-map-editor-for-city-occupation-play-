# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import numpy as np
import math
import base64
import zlib
import struct
import re

import rwgraphsub
 
def bytes_to_int_array(bytes_array)->list[int]:
    '''

    Parameters
    ----------
    bytes_array

    Returns
    -------
    int_array : list[int]
        4 bytes for 1 int

    '''

    if len(bytes_array) % 4 != 0:
        bytes_array += b'\0' * (4 - (len(bytes_array) % 4))

    int_array = struct.unpack('i' * (len(bytes_array) // 4), bytes_array)
    return int_array

class Coordinate:
    
    def __init__(self, x=0, y=0):
        self.content = np.array([[0], [0]], dtype=float)
        self.content[0][0] = x
        self.content[1][0] = y

    def x(self):
        return self.content[0][0]

    def y(self):
        return self.content[1][0]

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x() + other.x(), self.Y() + other.Y())
        else:
            return Coordinate(other + self.X(), other + self.Y())

    def __mul__(self, other):
        ans = Coordinate(0, 0)
        if isinstance(other, Coordinate):
            new_content = other.content * self.content
        elif isinstance(other, np.matrix) or (isinstance(other, np.ndarray) and other.ndim == 2):
            new_content = other @ self.content
        else:
            new_content = other * self.content
        ans.content = new_content
        return ans

    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.X() - other.X(), self.Y() - other.Y())
        else:
            return Coordinate(self.X() - other, self.Y() - other)

    def __neg__(self):
        return Coordinate(-self.X(), -self.Y())

squareType_matrixChange: dict[str, np.ndarray] = {
    'hex_x': np.array([[1, -1/2], [0, -1]], dtype=float)}

def remove_comments(code):
    
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    
    code = re.sub(r"'''[^']*?(?='''|\.\n)|\"\"\"[^']*?(?=\"\"\"|\.\n)", '', code)
    return code.strip()

class TypeName:
    zh_name: str
    zh_expression_name: str
    graph_name: str
    graph_detect_name: str
    isbuilding: bool

    def __init__(self, zh_name, zh_expression_name, graph_name, graph_detect_name, isbuilding):
        self.zh_name = zh_name
        self.zh_expression_name = zh_expression_name
        self.graph_name = graph_name
        self.graph_detect_name = graph_detect_name
        self.isbuilding = isbuilding

class RWGraph:
    def __init__(self, graph_file: str, grid_pixel, graph_grid, teamnum, teamgroup, default_name_file = './RWgraph_sub/RWgraph_sub_default_name.txt', personal_name_file = None):
        self.xmltree = et.ElementTree(file=graph_file)
        self.root = self.xmltree.getroot()
        self.grid_pixel = grid_pixel
        self.graph_grid = graph_grid
        self.teamnum = teamnum
        self.teamgroup = teamgroup
        self.inputName_TypeName = self.rwUnitNameDict(default_name_file, personal_name_file)
        for tag in self.root:
            if (tag.tag == "objectgroup") and (tag.attrib.get("name") == "Triggers"):
                self.TriggersElement = tag
                
    @staticmethod
    def rwUnitNameDict(default_name_file = './RWgraph_sub/RWgraph_sub_default_name.txt', personal_name_file = None):
        inputName_TypeName = {}
        with open(default_name_file, 'r', encoding = 'utf-8') as file:
            default_name_matrix = file.read()
            default_name_matrix = remove_comments(default_name_matrix)
            default_name_list = default_name_matrix.split('\n')
            for default_name in default_name_list:
                default_name_sep = default_name.split(' ')
                if len(default_name_sep) < 4:
                    continue
                for one_default_name in default_name_sep:
                    one_default_name.strip()
                inputName_TypeName[default_name_sep[0]] = TypeName(default_name_sep[1], default_name_sep[1], default_name_sep[0], default_name_sep[3], bool(default_name_sep[2]))

        if personal_name_file == None:
            with open(personal_name_file, 'r', encoding = 'utf-8') as file:
                default_name_matrix = file.read()
                default_name_matrix = remove_comments(default_name_matrix)
                default_name_list = default_name_matrix.split('\n')
                for default_name in default_name_list:
                    default_name_sep = default_name.split(' ')
                    if len(default_name_sep) < 2:
                        continue
                    for one_default_name in default_name_sep:
                        one_default_name.strip()
                    oldTypeName = inputName_TypeName[default_name_sep[0]]
                    inputName_TypeName[default_name_sep[2]] = TypeName(oldTypeName.zh_name, default_name_sep[1], oldTypeName.graph_name, oldTypeName.graph_detect_name)
                inputName_TypeName.pop(default_name_sep[0])
        return inputName_TypeName
    
    def addObject(self, tobject_attrib: dict[str, str], properties_dict: dict[str, str], otherItems_list: dict[dict[str, dict[str, str]], dict[str, dict[str, str]]] = {}):
        objectElement = self.TriggersElement.makeelement(
            'object', tobject_attrib)
        self.TriggersElement.append(objectElement)
        if properties_dict != []:
            propertiesElement = objectElement.makeelement('properties', {})
            objectElement.append(propertiesElement)
            for nproperty_name, nproperty_value in properties_dict.items():
                propertyElement = propertiesElement.makeelement(
                    'property', {'name': nproperty_name, 'value': nproperty_value})
                propertiesElement.append(propertyElement)
        if otherItems_list != {}:
            for other_NameAttrib, other_Child in otherItems_list.items():
                Items = objectElement.makeelement(
                    other_NameAttrib[0], other_NameAttrib.values()[0])
                objectElement.append(Items)
                for child_Name, child_attrib in other_Child.items():
                    childItems = Items.makeelement(child_Name, child_attrib)
                    Items.append(childItems)
        return objectElement
    
    def strall(self, depth, existtext = -1):
        strallans = ''
        element_list = [self.root]
        index_list = [0]
        while element_list != []:
            if index_list[-1] == 0:
                strallans = strallans + '\t' * (len(element_list) - 1) + str(element_list[-1].tag) + str(element_list[-1].attrib)
                if element_list[-1].text != None and str(element_list[-1].text).strip() != '':
                    strallans = strallans + '[' + str(element_list[-1].text)[0:existtext] + ']'
                strallans = strallans + '\n' 
            if len(element_list) < depth and index_list[-1] < len(element_list[-1]):
                element_list.append(element_list[-1][index_list[-1]])
                index_list[-1] = index_list[-1] + 1
                index_list.append(0)
            else:
                element_list = element_list[:-1]
                index_list = index_list[:-1]
        return strallans
    
    def decodelayer(self, layername):
        for layer in self.root:
            if layer.attrib.get("name") == layername:
                for data in layer:
                    return bytes_to_int_array(zlib.decompress(base64.b64decode(data.text)))
    
    @staticmethod
    def printObject(tobject):
        print('>tobject start')
        print('>attrib')
        for tobject_name, tobject_value in tobject.attrib.items():
            print(tobject_name + ':' + tobject_value)
        print('>property')
        for tobject_properties in tobject:
            if tobject_properties.tag == 'properties':
                for tobject_property in tobject_properties:
                    print(tobject_property.attrib['name'] + ':' + tobject_property.attrib['value'])
        print('>tobject end')
    
    def deleteObject(self, tobject):
        self.TriggersElement.remove(tobject)
        
    def deleteObject_partname(self, partname: str):
        boolfinish: bool = False
        while boolfinish == False:
            boolfinish = True
            for tobject in self.TriggersElement:
                if tobject.attrib['name'].find(partname) != -1:
                    self.deleteObject(tobject)
                    boolfinish = False
        self.IDreset_IDneqid()
    
    def IDreset_IDneqid(self):
        nowid = 1
        for tobject in self.TriggersElement:
            tobject.attrib['id'] = str(nowid)
            nowid = nowid + 1

    def emptyIDresetfront_IDneqid(self):
        for tobject in self.TriggersElement:
            if tobject.attrib.get('name') == None or tobject.attrib['name'] == '':
                self.TriggersElement.remove(tobject)
                self.TriggersElement.insert(0, tobject)

    def outputFile(self, graph_file: str):
        self.xmltree.write(graph_file)

    @staticmethod
    def changeTriggersProperty(tobject, name, value):
        for properties in tobject:
            if properties.tag == "properties":
                for nproperty in properties:
                    if nproperty.attrib['name'] == name:
                        nproperty.attrib['value'] = value
                        return
                aproperty = properties.makeelement(
                    'property', {'name': name, 'value': value})
                properties.append(aproperty)

    @staticmethod
    def returnTriggersProperty(tobject, name):
        for properties in tobject:
            if properties.tag == "properties":
                for nproperty in properties:
                    if nproperty.attrib['name'] == name:
                        return nproperty.attrib['value']

    def teamRank(self, teamnow):
        return math.floor(teamnow / self.teamgroup)
    
    def teamGroup(self, teamnow):
        return teamnow % self.teamgroup
    
    def neighborTeam(self, teamnow):
        teamranknow = self.teamRank(teamnow)
        teamgroupnow = self.teamGroup(teamnow)
        if self.teamgroup == 1:
            return None
        else:
            teamgroupset = set([teamgroup + teamranknow * self.teamgroup for teamgroup in range(self.teamgroup) if teamgroup != teamgroupnow])
            if self.teamgroup == 2:
                return teamgroupset[0]
            else:
                return teamgroupset
            



    
    


