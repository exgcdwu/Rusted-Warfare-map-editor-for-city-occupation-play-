
class LoadError(SyntaxError):
    pass

class KeyConflictError(KeyError):
    pass

class CoordinateIndexError(IndexError):
    pass

class ObjectNameError(KeyError):
    pass

class CoordinateDimError(IndexError):
    pass

class BuildingDetectError(ValueError):
    pass

class TileGroupMatrixListOfListError(ValueError):
    pass