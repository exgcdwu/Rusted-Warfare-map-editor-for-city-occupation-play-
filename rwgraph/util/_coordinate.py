import numpy as np
class Coordinate:
    
    def __init__(self, x:int = 0, y:int = 0):
        self.content = np.array([[0], [0]], dtype=float)
        self.content[0][0] = x
        self.content[1][0] = y

    def x(self):
        return self.content[0][0]

    def y(self):
        return self.content[1][0]

    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x() + other.x(), self.y() + other.y())
        else:
            return Coordinate(other + self.x(), other + self.y())

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
            return Coordinate(self.x() - other.x(), self.y() - other.y())
        else:
            return Coordinate(self.x() - other, self.y() - other)

    def __neg__(self):
        return Coordinate(-self.x(), -self.y())