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
    
    def iterator(self):
        for i in range(0, self._addCoordinate.x()):
            for j in range(0, self._addCoordinate.y()):
                yield self._initialCoordinate + Coordinate(i, j)
