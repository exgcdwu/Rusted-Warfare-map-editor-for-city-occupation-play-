import numpy as np
from copy import deepcopy
import math

import rwmap._exceptions as rwexceptions

class Coordinate:
    pass

class Coordinate:
    
    def __init__(self, x:int = 0, y:int = 0, dtype:str = np.int32):
        self._content = np.array([[0], [0]], dtype=dtype)
        self._content[0][0] = x
        self._content[1][0] = y

    @classmethod
    def init_np(cls, content:np.ndarray):
        if content.shape == (2, 1):
            return cls(deepcopy(content[0][0]), deepcopy(content[1][0]), dtype = content.dtype)
        else:
            raise rwexceptions.CoordinateDimError(str(content))

    @classmethod
    def init_id(cls, id:int, column:int):
        return cls(math.floor(id / column), id % column)

    def x(self):
        return deepcopy(self._content[0][0])

    def y(self):
        return deepcopy(self._content[1][0])
    
    def dtype(self):
        return deepcopy(self._content.dtype)
    
    def id(self, width:int)->int:
        return int(self.x() * width + self.y())
    
    def output_tuple(self)->tuple:
        return (self.x(), self.y())
    
    def transpose(self)->Coordinate:
        return Coordinate(self.y(), self.x(), self._content.dtype)

    def changetype(self, dtype)->Coordinate:
        return Coordinate(self.x(), self.y(), dtype)
    
    def mul(self):
        return self.x() * self.y()
    
    def sum(self):
        return self.x() + self.y()
    
    def dis(self)->float:
        return math.sqrt(self.x() ** 2 + self.y() ** 2)
    
    def vertical(self)->Coordinate:
        return Coordinate(self.y(), -self.x(), self._content.dtype)
    
    def unit(self)->Coordinate:
        return self.changetype(np.float64) / self.dis()

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x() + other.x(), self.y() + other.y(), self._content.dtype)
        else:
            return Coordinate(other + self.x(), other + self.y(), self._content.dtype)

    def __mul__(self, other):
        ans = Coordinate(0, 0)
        if isinstance(other, Coordinate):
            new_content = other._content * self._content
        elif isinstance(other, np.matrix) or (isinstance(other, np.ndarray) and other.ndim == 2):
            new_content = other @ self._content
        else:
            new_content = other * self._content
        ans._content = new_content
        return ans
    
    def __truediv__(self, other):
        ans = Coordinate(0, 0)
        if isinstance(other, Coordinate):
            new_content = self._content / other._content
        else:
            new_content = self._content / other
        ans._content = new_content
        return ans
    
    def __floordiv__(self, other):
        ans = Coordinate(0, 0)
        if isinstance(other, Coordinate):
            new_content = self._content // other._content
        else:
            new_content = self._content // other
        ans._content = new_content
        return ans
    
    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x() - other.x(), self.y() - other.y(), self._content.dtype)
        else:
            return Coordinate(self.x() - other, self.y() - other, self._content.dtype)

    def __neg__(self):
        return Coordinate(-self.x(), -self.y(), self._content.dtype)
    
    def _iterator(self):
        for i in range(0, self.x()):
            for j in range(0, self.y()):
                yield Coordinate(i, j, self._content.dtype)

    def __iter__(self):
        return self._iterator()
    
    def __lt__(self, other)->int:
        if self.x() < other.x() and self.y() < other.y():
            return 1
        elif self.x() > other.x() and self.y() > other.y():
            return -1
        else:
            return 0
        
    def contain(self, other:Coordinate)->bool:
        if isinstance(other, Coordinate):
            return other.x() < self.x() and other.y() < self.y()
        else:
            raise ValueError(f"Coordinate __contain__: not Coordinate")

    def __contain__(self, other:Coordinate)->bool:
        return self.contain(other)
        
    def out_contain(self, other:Coordinate)->bool:
        if isinstance(other, Coordinate):
            return other.x() > self.x() and other.y() > self.y()
        else:
            raise ValueError(f"Coordinate _out_contain: not Coordinate")

    def output_str(self)->str:
        str_now = "Coordinate:(" + f"{self.x():.2f}" + "," + f"{self.y():.2f}" + "," + "dtype = " + str(self.dtype()) + ")"
        return str_now
    
    def __repr__(self)->str:
        return self.output_str()
    
class Rectangle:
    pass

class Rectangle:
    def __init__(self, initialCoordinate:Coordinate, addCoordinate:Coordinate):
        self._initialCoordinate = deepcopy(initialCoordinate)
        self._addCoordinate = deepcopy(addCoordinate)
    
    def i(self):
        return deepcopy(self._initialCoordinate)

    def a(self):
        return deepcopy(self._addCoordinate)
    
    def e(self):
        return deepcopy(self._initialCoordinate + self._addCoordinate)
    
    def transpose(self)->Rectangle:
        return Rectangle(self._initialCoordinate.transpose(), self._addCoordinate.transpose())
    
    @classmethod
    def init_ae(cls, initialCoordinate:Coordinate, endCoordinate:Coordinate):
        addCoordinate = endCoordinate - initialCoordinate
        return cls(initialCoordinate, addCoordinate)

    def _iterator(self):
        for i in range(self.i().x(), self.e().x()):
            for j in range(self.i().y(), self.e().y()):
                yield Coordinate(i, j)

    def __iter__(self):
        return self._iterator()
    
    def __add__(self, other):
        if isinstance(other, Rectangle):
            return Rectangle(self._addCoordinate + other._addCoordinate, self._initialCoordinate + other._initialCoordinate)
        elif isinstance(other, Coordinate):
            return Rectangle(self._initialCoordinate, self._addCoordinate + other)
    
    def __sub__(self, other):
        if isinstance(other, Rectangle):
            return Rectangle(self._initialCoordinate - other._initialCoordinate, self._addCoordinate - other._addCoordinate)
        elif isinstance(other, Coordinate):
            return Rectangle(self._initialCoordinate, self._addCoordinate - other)

    def __neg__(self):
        return Rectangle(-self._initialCoordinate, -self._addCoordinate)
    
    def contain(self, other:Coordinate)->bool:
        if isinstance(other, Coordinate):
            return self.i().out_contain(other) and other in self.e()
        else:
            raise ValueError(f"Coordinate __contain__: not Coordinate")
        
    
    def __contain__(self, other:Coordinate)->bool:
        return self.contain(other)
        
    def output_str(self)->str:
        str_now = "Rectangle:(" + str(self.i().output_tuple()) + "-" + str(self.e().output_tuple()) + ")"
        return str_now
    
    def __repr__(self)->str:
        return self.output_str()
    
class TagCoordinate(Coordinate):
    pass

class TagCoordinate(Coordinate):
    def __init__(self, tag:str, place:Coordinate):
        self.__dict__ = deepcopy(place.__dict__)
        self._tag = tag

    @classmethod
    def init_xy(cls, tag:str, x = 0, y = 0, dtype:str = np.int32):
        return cls(tag, Coordinate(x, y, dtype))
    
    @classmethod
    def init_np(cls, tag:str, content:np.ndarray):
        return cls(tag, Coordinate.init_np(content))

    @classmethod
    def init_id(cls, tag:str, id:int, column:int):
        return cls(tag, Coordinate.init_id(id, column))

    def tag(self):
        return self._tag
    
    def place(self):
        return Coordinate.init_np(self._content)
    
    def transpose(self)->TagCoordinate:
        return TagCoordinate(self._tag, Coordinate.transpose(self))
    
    def __add__(self, other):
        return TagCoordinate(deepcopy(self._tag), Coordinate.__add__(self, other))

    def __mul__(self, other):
        return TagCoordinate(deepcopy(self._tag), Coordinate.__mul__(self, other))
    
    def __truediv__(self, other):
        return TagCoordinate(deepcopy(self._tag), Coordinate.__truediv__(self, other))
    
    def __floordiv__(self, other):
        return TagCoordinate(deepcopy(self._tag), Coordinate.__floordiv__(self, other))
    
    def __sub__(self, other):
        return TagCoordinate(deepcopy(self._tag), Coordinate.__sub__(self, other))

    def __neg__(self, other):
        return TagCoordinate(deepcopy(self._tag), Coordinate.__neg__(self, other))
    
    def _iterator(self):
        for coo in Coordinate._iterator(self):
            yield TagCoordinate(deepcopy(self._tag), coo)
    
class TagRectangle(Rectangle):
    pass

class TagRectangle(Rectangle):
    def __init__(self, tag:str, place:Rectangle):
        self._initialCoordinate = deepcopy(place._initialCoordinate)
        self._addCoordinate = deepcopy(place._addCoordinate)
        self._tag = tag

    def tag(self)->str:
        return self._tag

    @classmethod
    def init_ae(cls, tag:str, initialCoordinate:Coordinate, endCoordinate:Coordinate):
        return cls(tag, Rectangle.init_ae(initialCoordinate, endCoordinate))
    
    def rectangle(self)->Rectangle:
        return Rectangle(deepcopy(self._initialCoordinate), deepcopy(self._addCoordinate))
    
    def transpose(self)->TagRectangle:
        return TagRectangle(self._tag, Rectangle.transpose(self))

    def i(self):
        return TagCoordinate(self._tag, deepcopy(self._initialCoordinate))

    def a(self):
        return TagCoordinate(self._tag, deepcopy(self._addCoordinate))
    
    def e(self):
        return TagCoordinate(self._tag, self._initialCoordinate + self._addCoordinate)

    def _iterator(self):
        for i in range(0, self._addCoordinate.x()):
            for j in range(0, self._addCoordinate.y()):
                coordinate_now = self._initialCoordinate + Coordinate(i, j)
                yield TagCoordinate(self._tag, coordinate_now)

    def __iter__(self):
        return self._iterator()
