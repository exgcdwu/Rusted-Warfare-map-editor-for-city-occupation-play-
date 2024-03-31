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
import os
from typing import Union
 
def bytes_to_int_array(bytes_array:bytes)->list[int]:
    '''
    4 bytes for 1 int
    Parameters
    ----------
    bytes_array : bytes

    Returns
    -------
    int_array : list[int]


    '''

    if len(bytes_array) % 4 != 0:
        bytes_array += b'\0' * (4 - (len(bytes_array) % 4))

    int_array = struct.unpack('i' * (len(bytes_array) // 4), bytes_array)
    return int_array

class Coordinate:
    
    def __init__(self, x, y, dtype = 'int32')->None:
        '''
        Initialization of RW map Coordinate
        
        Parameters
        ----------
        x : number
        y : number
        dtype : str, the type of number

        Returns
        -------
        None.

        '''
        self.content = np.array([[x], [y]], dtype = dtype)

    def x(self):
        '''
        x of the Coordiante
        
        Returns
        -------
        number
            
        '''
        return self.content[0][0]

    def y(self):
        '''
        y of the Coordiante
        
        Returns
        -------
        number
            
        '''
        return self.content[1][0]

    def __add__(self, other):
        '''

        Parameters
        ----------
        other : 
            number: add to x and y
            Coordiante: add them seperately

        Returns
        -------
        Coordinate

        '''
        if isinstance(other, Coordinate):
            return Coordinate(self.x() + other.x(), self.Y() + other.Y())
        else:
            return Coordinate(other + self.X(), other + self.Y())

    def __mul__(self, other):
        '''

        Parameters
        ----------
        other : 
            number: multiply to x and y
            Coordiante: multiply them seperately
            np.matrix or np.ndarray: matrix multiplication
        Returns
        -------
        Coordinate

        '''
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
        '''

        Parameters
        ----------
        other : 
            number: subtract other from x and y
            Coordiante: substract other from self seperately

        Returns
        -------
        Coordinate

        '''
        if isinstance(other, Coordinate):
            return Coordinate(self.X() - other.X(), self.Y() - other.Y())
        else:
            return Coordinate(self.X() - other, self.Y() - other)

    def __neg__(self):
        '''
        Negative Coordinate
        
        Returns
        -------
        Coordinate

        '''
        return Coordinate(-self.X(), -self.Y())

def remove_comments(code:str)->str:
    '''
    Remove python style comments of a string
    
    e.g. \# ...
    \'\'\'
    ...
    \'\'\'
    
    Parameters
    ----------
    code : str

    Returns
    -------
    str

    '''
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r"'''[^']*?(?='''|\.\n)|\"\"\"[^']*?(?=\"\"\"|\.\n)", '', code)
    return code.strip()

class TypeName:
    
    def __init__(self, zh_name:str, zh_expression_name:str, graph_name:str, graph_detect_name:str, isbuilding:bool)->None:
        '''
        Initialization of TypeName

        Parameters
        ----------
        zh_name : str
            Chinese official name of a unit of RW 
        zh_expression_name : str
            Chinese personal name of a unit of RW
        graph_name : str
            Official nome of a unit of RW map editor
        graph_detect_name : str
            Some unit names separated by ',' which can be updated from a unit, for unitType of trigger(unitDetect)
        isbuilding : bool
            Whether it's building or not

        Returns
        -------
        None.

        '''
        self.zh_name = zh_name
        self.zh_expression_name = zh_expression_name
        self.graph_name = graph_name
        self.graph_detect_name = graph_detect_name
        self.isbuilding = isbuilding

squareType_matrixChange: dict[str, np.ndarray] = {
    'hex_x': np.array([[1, -1/2], [0, -1]], dtype='double')}
#square deformation matrix for different tag

current_dir = os.path.dirname(__file__)
current_dir_sub = current_dir + "\\RWgraph_sub\\"
current_default_name_file = current_dir_sub + "RWgraph_sub_default_name.txt"
current_personal_name_file = current_dir_sub + "RWgraph_sub_name.txt"

class RWGraph:
    
    def __init__(self, graph_file:str, teamnum:int = 2, teamgroup:int = 2, default_name_file:str = current_default_name_file, personal_name_file:str = current_personal_name_file)->None:
        self.xmltree = et.ElementTree(file=graph_file)
        self.root = self.xmltree.getroot()
        
        self.version = self.root.attrib['version']
        self.tiledversion = self.root.attrib['tiledversion']
        
        self.grid_pixel = Coordinate(int(self.root.attrib['tilewidth']), int(self.root.attrib['tileheight']))
        self.graph_grid = Coordinate(int(self.root.attrib['width']), int(self.root.attrib['height']))      
        
        self.inputName_TypeName = self.__rwUnitNameDict(default_name_file, personal_name_file)
        
        for tag in self.root:
            if (tag.tag == "objectgroup") and (tag.attrib.get("name") == "Triggers"):
                self.TriggersElement = tag
    # @overload
    # def __init__(self, grid_pixel:Coordinate, graph_grid:Coordinate, teamnum:int, teamgroup:int, default_name_file:str, personal_name_file:str = None, version:str = '1.10', tiledversion:str = '1.10.2')->None:
    #     '''
    #     No original graph file
    #     Build a map xml tree

    #     Parameters
    #     ----------
    #     grid_pixel : Coordinate
    #         DESCRIPTION.
    #     graph_grid : Coordinate
    #         DESCRIPTION.
    #     teamnum : int
    #         DESCRIPTION.
    #     teamgroup : int
    #         DESCRIPTION.
    #     default_name_file : str
    #         DESCRIPTION.
    #     personal_name_file : str, optional
    #         DESCRIPTION. The default is None.
    #     version : str, optional
    #         DESCRIPTION. The default is '1.10'.
    #     tiledversion : str, optional
    #         DESCRIPTION. The default is '1.10.2'.

    #     Returns
    #     -------
    #     None
    #         DESCRIPTION.

    #     '''
    #     self.root = et.Element("map", {'version': version, 'tiledversion': tiledversion, 'orientation': 'orthogonal', 'renderorder': 'right-down', 'width': graph_grid.x(), 'height': graph_grid.y(), 'tilewidth': grid_pixel.x(), 'tileheight': grid_pixel.y(), 'infinite': '0', 'nextlayerid': '1', 'nextobjectid': '1'})
    #     self.xmltree = et.ElementTree(self.root)
    #     self.addLayer('Ground')
    #     self.addLayer('Units')
    #     self.addLayer('Items')
    #     self.addObjectgroup('Triggers')
        
    #     self.version = version
    #     self.tiledversion = tiledversion
    #     self.grid_pixel = grid_pixel
    #     self.graph_grid = graph_grid
    #     self.teamnum = teamnum
    #     self.teamgroup = teamgroup
    #     self.inputName_TypeName = self.__rwUnitNameDict(default_name_file, personal_name_file)
    #     for tag in self.root:
    #         if (tag.tag == "objectgroup") and (tag.attrib.get("name") == "Triggers"):
    #             self.TriggersElement = tag
    # @overload
    # def __init__(self, graph_file: str, teamnum:int, teamgroup:int, default_name_file:str, personal_name_file:str = None)->None:
    #     self.xmltree = et.ElementTree(file=graph_file)
    #     self.root = self.xmltree.getroot()
        
    #     self.version = self.root.attrib['version']
    #     self.tiledversion = self.root.attrib['tiledversion']
        
    #     self.grid_pixel = Coordinate(int(self.root.attrib['tilewidth']), int(self.root.attrib['tileheight']))
    #     self.graph_grid = Coordinate(int(self.root.attrib['width']), int(self.root.attrib['height']))
    #     self.teamnum = teamnum
    #     self.teamgroup = teamgroup
    #     self.inputName_TypeName = self.__rwUnitNameDict(default_name_file, personal_name_file)
    #     for tag in self.root:
    #         if (tag.tag == "objectgroup") and (tag.attrib.get("name") == "Triggers"):
    #             self.TriggersElement = tag
    
    def __newLayerid(self)->int:
        newlayerid = int(self.root.attrib['nextlayerid'])
        self.root.attrib['nextlayerid'] = str(int(self.root.attrib['nextlayerid']) + 1)
        return newlayerid
   
    def addLayer(self, layername:str)->et.Element:
        layerid = self.__newLayerid()
        layerelement = self.root.makeelement('layer', {'id':str(layerid), 'name': layername, 'width': str(self.graph_grid.x()), 'height': str(self.graph_grid.y())})
        self.root.append(layerelement)
        return layerelement
        
    def addObjectgroup(self, objectgroupname:str)->et.Element:
        layerid = self.__newLayerid()
        layerelement = self.root.makeelement('objectgroup', {'id':str(layerid), 'name': objectgroupname})
        self.root.append(layerelement)
        return layerelement
    
    def __newobjectid(self)->int:
        newobjectid = int(self.root.attrib['nextobjectid'])
        self.root.attrib['nextobjectid'] = str(int(self.root.attrib['nextobjectid']) + 1)
        return newobjectid
    
    def __resetmaxobjectid(self, maxid:int)->None:
        self.root.attrib['nextobjectid'] = maxid
    
    
    
    @staticmethod
    def __rwUnitNameDict(default_name_file:str, personal_name_file:str = None)->dict[str, TypeName]:
        '''
        Create name dictionary for __init__

        Parameters
        ----------
        default_name_file : str
            The path of default units' name file.
            The example is in RWgraph_sub/RWgraph_sub_default_name.txt.
        personal_name_file : str, optional
            The path of personal units' name file. The default is None.
            The example is in RWgraph_sub/RWgraph_sub_name.txt.

        Returns
        -------
        inputName_TypeName : dict[str, TypeName]
            the unit dictionary of this graph

        '''
        if default_name_file != None:
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

        if personal_name_file != None:
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
    
    @staticmethod
    def strall(etElement:et.Element, depth:int, existtext:int = -1)->str:
        '''
        Present a node of the .tmx file. It is suitable for reading in .txt. 

        Parameters
        ----------
        etElement : et.Element
            The node.
        depth : int
            The maximum depth of node which would output.
        existtext : int, optional
            The maximum length of text which would output. The default is -1, no output limit.

        Returns
        -------
        str
            A string for reading.

        '''
        strallans = ''
        element_list = [etElement]
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
    
    def decodeLayer(self, layername:str)->np.ndarray:
        '''
        Decode a layer into an array of grid id.

        Parameters
        ----------
        layername : str

        Returns
        -------
        np.ndarray
        
        ndim = 2
        width = self.graph_grid.x()
        height = self.graph_grid.y()
        Tile id matrix of the layer

        '''
        for layer in self.root:
            if layer.attrib.get("name") == layername:
                for data in layer:
                    int_list = bytes_to_int_array(zlib.decompress(base64.b64decode(data.text)))
        grid_matrix = np.array(int_list)
        
        grid_matrix = np.reshape(grid_matrix, [self.graph_grid.x(), self.graph_grid.y()])
        print(type(grid_matrix))
        return grid_matrix
    
    def addObject(self, tobject_attrib: dict[str, str], properties_dict: dict[str, str], otherItems_list: dict[dict[str, dict[str, str]], dict[str, dict[str, str]]] = {})->et.Element:
        '''
        Add an object to the layer 'Triggers'

        Parameters
        ----------
        tobject_attrib : dict[str, str]
            The default properties of this object
        properties_dict : dict[str, str]
            The optional properties of this object
        otherItems_list : dict[dict[str, dict[str, str]], dict[str, dict[str, str]]], optional
            The other properties of this object. The default is {}.

        Returns
        -------
        objectElement : et.Element
            The object 

        '''
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
        print(type(objectElement))
        return objectElement
    
    @staticmethod
    def strObject(tobject:et.Element)->str:
        '''
        Present an Object from Triggers
        Parameters
        ----------
        tobject : et.Element
        
        Returns
        -------
        str

        '''
        strtobjectans = '>tobject start'
        strtobjectans = strtobjectans + '>attrib'
        for tobject_name, tobject_value in tobject.attrib.items():
            strtobjectans = strtobjectans + tobject_name + ':' + tobject_value
        strtobjectans = strtobjectans + '>property'
        for tobject_properties in tobject:
            if tobject_properties.tag == 'properties':
                for tobject_property in tobject_properties:
                    strtobjectans = strtobjectans + tobject_property.attrib['name'] + ':' + tobject_property.attrib['value']
        strtobjectans = strtobjectans + '>tobject end'
        return strtobjectans
    
    def deleteObject(self, tobject:et.Element)->None:
        '''
        Delete an Object from Triggers

        Parameters
        ----------
        tobject : et.Element

        Returns
        -------
        None

        '''
        self.TriggersElement.remove(tobject)
        
    def deleteObject_partname(self, partname: str)->None:
        '''
        Delete some objects by overlap of the partname

        Parameters
        ----------
        partname : str

        Returns
        -------
        None.

        '''
        boolfinish: bool = False
        while boolfinish == False:
            boolfinish = True
            for tobject in self.TriggersElement:
                if tobject.attrib['name'].find(partname) != -1:
                    self.deleteObject(tobject)
                    boolfinish = False
        self.IDreset_IDneqid()
    
    def IDreset_IDneqid(self)->None:
        '''
        Reset ID of all objects of Triggers if IDs(default) do not equal to ids(alsoactivate).

        Returns
        -------
        None.

        '''
        nowid = 1
        for tobject in self.TriggersElement:
            tobject.attrib['id'] = str(nowid)
            nowid = nowid + 1

    def emptyIDresetfront_IDneqid(self)->None:
        '''
        Some object with empty name will be advanced in the file.

        Returns
        -------
        None.

        '''
        for tobject in self.TriggersElement:
            if tobject.attrib.get('name') == None or tobject.attrib['name'] == '':
                self.TriggersElement.remove(tobject)
                self.TriggersElement.insert(0, tobject)

    def outputFile(self, graph_file: str)->None:
        '''
        Output the RWGraph class to a new RW graph file.

        Parameters
        ----------
        graph_file : str
            The path of your new graph.

        Returns
        -------
        None.

        '''
        self.xmltree.write(graph_file)

    @staticmethod
    def changeObjectProperty(tobject:et.Element, name:str, value:str)->None:
        '''
        Change(or add if there'\s no this property) a property of an object from Triggers.

        Parameters
        ----------
        tobject : et.Element
        name : str
            The name of the property
        value : str
            The value of the property

        Returns
        -------
        None.

        '''
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
    def returnTriggersProperty(tobject:et.Element, name:str)->None:
        '''
        Return the value of an object's property by name.

        Parameters
        ----------
        tobject : et.Element
        name : str
            The name of the property

        Returns
        -------
        None.

        '''
        for properties in tobject:
            if properties.tag == "properties":
                for nproperty in properties:
                    if nproperty.attrib['name'] == name:
                        return nproperty.attrib['value']

    def teamRank(self, teamnow:int)->int:
        '''
        A player\'s rank from the same group by its team.

        Parameters
        ----------
        teamnow : int
            its team

        Returns
        -------
        int
            its rank from the same group.

        '''
        return math.floor(teamnow / self.teamgroup)
    
    def teamGroup(self, teamnow:int)->int:
        '''
        A player\'s group by its team.

        Parameters
        ----------
        teamnow : int
            its team

        Returns
        -------
        int
            its group

        '''
        return teamnow % self.teamgroup
    
    def neighborTeam(self, teamnow:int)->Union[set[int], int, None]:
        '''
        A player's enemy which has the same rank.

        Parameters
        ----------
        teamnow : int
            its team

        Returns
        -------
        (Union[set[int], int, None])
            Its enemy team which has the same rank.
            Return type is int if only one enemy.
            Return None if no enemy.

        '''
        teamranknow = self.teamRank(teamnow)
        teamgroupnow = self.teamGroup(teamnow)
        if self.teamgroup == 1:
            return None
        else:
            teamgroupset = set([teamgroup + teamranknow * self.teamgroup for teamgroup in range(self.teamgroup) if teamgroup != teamgroupnow])
            if self.teamgroup == 2:
                return teamgroupset.pop()
            else:
                return teamgroupset
            



    
    


