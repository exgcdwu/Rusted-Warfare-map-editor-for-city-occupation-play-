import rwmap._frame as frame


def point_list_to_str(point_list:list[frame.Coordinate])->str:
    str_ans = ""
    for point in point_list:
        str_ans = str_ans + str(point.x()) + "," + str(point.y()) + " "
    return str_ans