import numpy as np
class Coordinate:
    
    def __init__(self, x:int = 0, y:int = 0, dtype:str = np.int32):
        self._content = np.array([[0], [0]], dtype=dtype)
        self._content[0][0] = x
        self._content[1][0] = y

    def x(self):
        return self._content[0][0]

    def y(self):
        return self._content[1][0]
    
    def id(self, width:int)->int:
        return int(self.y() * width + self.x())

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x() + other.x(), self.y() + other.y())
        else:
            return Coordinate(other + self.x(), other + self.y())

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

    def __sub__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x() - other.x(), self.y() - other.y())
        else:
            return Coordinate(self.x() - other, self.y() - other)

    def __neg__(self):
        return Coordinate(-self.x(), -self.y())
    
    def _iterator(self):
        for i in range(0, self.x()):
            for j in range(0, self.y()):
                yield Coordinate(i, j)

    def __iter__(self):
        return self._iterator()
    
    def __lt__(self, other)->int:
        if self.x() < other.x() and self.y() < other.y():
            return 1
        elif self.x() > other.x() and self.y() > other.y():
            return -1
        else:
            return 0
    
class Rectangle:
    def __init__(self, initialCoordinate:Coordinate, addCoordinate:Coordinate):
        self._initialCoordinate = initialCoordinate
        self._addCoordinate = addCoordinate
    
    def i(self):
        return self._initialCoordinate

    def a(self):
        return self._addCoordinate
    
    def e(self):
        return self._initialCoordinate + self._addCoordinate
    
    def _iterator(self):
        for i in range(0, self._addCoordinate.x()):
            for j in range(0, self._addCoordinate.y()):
                coordinate_now = self._initialCoordinate + Coordinate(i, j)
                yield Coordinate(coordinate_now.x(), coordinate_now.y())

    def __iter__(self):
        return self._iterator()
    
class TagCoordinate:
    def __init__(self, tag:str, place:Coordinate):
        self._place = place
        self._tag = tag

    @classmethod
    def init_xy(cls, tag:str, x = 0, y = 0, dtype:str = np.int32):
        return cls(tag, Coordinate(x, y, dtype))

    def tag(self):
        return self._tag
    
    def place(self):
        return self._place
