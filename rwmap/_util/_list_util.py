
import rwmap._frame as frame

def fill_list_of_list(element, size:frame.Coordinate):
    return [[element] * size.y() for i in range(size.x())]