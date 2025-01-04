
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

class ElementOriNotFoundError(KeyError):
    pass

class ElementOriFoundMultiError(KeyError):
    pass

class LayerNotFoundError(KeyError):
    pass

class TileSetIndexError(IndexError):
    pass