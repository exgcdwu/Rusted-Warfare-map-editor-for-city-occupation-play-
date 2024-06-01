import rwmap as rw

def NESWbool_onetrue_direction(NESW:list[bool])->str:
    if NESW[0]:
        return "N"
    elif NESW[1]:
        return "E"
    elif NESW[2]:
        return "S"
    else:
        return "W"
    
def NESWbool_directionsymbol(NESW:list[bool])->str:
    dirsum = sum(NESW)
    if dirsum == 4:
        return "A"
    elif dirsum == 3:
        strn = "e"
        NESW_inv = [not boo for boo in NESW]
        return strn + NESWbool_onetrue_direction(NESW_inv)
    elif dirsum == 2:
        if NESW[0] and NESW[2]:
            return "V"
        elif NESW[1] and NESW[3]:
            return "H"
        strn = ("N" if NESW[0] else "S")
        strn = strn + ("E" if NESW[1] else "W")
        return strn
    elif dirsum == 1:
        return NESWbool_onetrue_direction(NESW)
    else:
        return "C"
    





def river_dict_one_direct(city_occu_tile_name:str, column:int, direction:str):
    column_n = rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, column * 3)
    river_dict_n = {
        "H": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 0), 
        "V": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 1), 
        "HB": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 1, 2), 
        "VB": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 2), 

        "NE": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 2, 0), 
        "NW": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 1, 1), 
        "SE": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 1, 0),  
        "SW": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 2, 1), 

        "eN": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 2, 2), 
        "eS": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 3, 2), 
        "eW": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 3, 0), 
        "eE": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 3, 1)
    }
    for name, value in river_dict_n.items():
        river_dict_n[name] = value + column_n
    other_river_dict = {
        "A": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 4, 12), 
        "F": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 5, 12)
    }

    item_river_dict = {
        "N": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 3, 12), 
        "S": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 1, 12), 
        "W": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 12), 
        "E": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 2, 12)
    }

    river_dict_temp = {**river_dict_n, **other_river_dict}
    river_dict_ans = {}
    for name, value in river_dict_temp.items():
        river_dict_ans[direction + "-b-" + name] = value
    
    river_dict_ans_item = {}
    for name, value in item_river_dict.items():
        river_dict_ans_item[direction + "-b-" + name] = value

    return [river_dict_ans, river_dict_ans_item]

def river_dict(city_occu_tile_name:str, column:int, direction:str):
    direction_list = direction.split(",")
    dict_item = {}
    dict_n = {}
    for direction_n in direction_list:
        direction_n = direction_n.strip()
        dict_temp = river_dict_one_direct(city_occu_tile_name, column, direction_n)
        dict_n.update(dict_temp[0])
        dict_item.update(dict_temp[1])
    dict_temp = river_dict_one_direct(city_occu_tile_name, column, "")
    dict_n.update(dict_temp[0])
    dict_item.update(dict_temp[1])
    return [dict_n, dict_item]

def river_map(river_NESbool:list[bool], riverNE_NESbool:list[bool], riverSE_NESbool:list[bool], railway_NESbool:list[bool]):
    river_map_n = {
            "NE-b-C": "-b-" + NESWbool_directionsymbol([False, riverNE_NESbool[2], river_NESbool[1], river_NESbool[0]]), 
            "SE-b-C": "-b-" + NESWbool_directionsymbol([river_NESbool[1], riverSE_NESbool[0], False, river_NESbool[2]])
        }
    if not railway_NESbool[0]:
        river_map_n.update({"NE-b-HB": "NE-b-H"})
    if not railway_NESbool[1]:
        river_map_n.update({"E-b-VB": "E-b-V"})
    if not railway_NESbool[2]:
        river_map_n.update({"SE-b-HB": "SE-b-H"})
    return river_map_n

def line_dict_one_direction(tile:rw.const.TYPE.tileid, direction:str):
    return {direction + '-l' :tile}

def line_dict(tile:rw.const.TYPE.tileid, direction:str):
    direction_list = direction.split(",")
    dict_n = {}
    for direction_n in direction_list:
        direction_n = direction_n.strip()
        dict_n.update(line_dict_one_direction(tile, direction_n))
    return dict_n

def line_map(N_CW_bool:list[bool]):
    N_CW_str = ["NE", "E", "SE", "SW", "W", "NW"]
    dict_n = {}
    for i in range(6):
        if not N_CW_bool[i]:
            dict_n.update({N_CW_str[i] + "-l-C":N_CW_str[i] + "-l"})
    return dict_n

def railway_dict_one_direction(city_occu_tile_name:str, direction:str):
    column_n = rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 15)
    river_dict_n = {
        "H": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 1), 
        "V": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 0), 

        "NE": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 2, 0), 
        "NW": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 2, 1), 
        "SE": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 1, 0),  
        "SW": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 1, 1), 

        "eN": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 3, 1), 
        "eS": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 4, 0), 
        "eW": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 3, 0), 
        "eE": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 4, 1), 

        "A": rw.frame.TagCoordinate.init_xy(city_occu_tile_name, 0, 2)
    }
    for name, value in river_dict_n.items():
        river_dict_n[name] = value + column_n
    river_dict_ans = {}
    for name, value in river_dict_n.items():
        river_dict_ans[direction + "-l-" + name] = value
    return river_dict_ans

def railway_dict(city_occu_tile_name:str, direction:str):
    direction_list = direction.split(",")
    dict_n = {}
    for direction_n in direction_list:
        direction_n = direction_n.strip()
        dict_n.update(railway_dict_one_direction(city_occu_tile_name, direction_n))
    
    return dict_n

def railway_map(N_CW_bool:list[bool]):
    N_CW_str = ["NE", "E", "SE", "SW", "W", "NW"]
    N_CW_bool_now = [
        [[False, True, True, False], [True, False, False, True]], 
        [[False, False, True, True], [True, True, False, True]], 
        [[False, False, True, True], [True, True, False, False]], 
        [[True, False, False, True], [False, True, True, False]], 
        [[True, True, False, False], [False, True, True, True]], 
        [[True, True, False, False], [False, False, True, True]]
    ]
    if N_CW_bool[0]:
        N_CW_bool_now[5][1][3] = True
        N_CW_bool_now[1][0][0] = True
    if N_CW_bool[1]:
        N_CW_bool_now[0][1][2] = True
        N_CW_bool_now[2][0][0] = True
    if N_CW_bool[2]:
        N_CW_bool_now[1][1][2] = True
        N_CW_bool_now[3][0][1] = True
    if N_CW_bool[3]:
        N_CW_bool_now[2][1][3] = True
        N_CW_bool_now[4][0][2] = True
    if N_CW_bool[4]:
        N_CW_bool_now[3][1][0] = True
        N_CW_bool_now[5][0][2] = True
    if N_CW_bool[5]:
        N_CW_bool_now[4][1][0] = True
        N_CW_bool_now[0][0][3] = True

    dict_n = {}
    for i in range(6):
        for j in range(2):
            dict_n.update({N_CW_str[i] + "-l-C-" + \
                           N_CW_str[(i + 2 * j + 5) % 6]: N_CW_str[i] + "-l-" + \
                            NESWbool_directionsymbol(N_CW_bool_now[i][j])})
    return dict_n



def str_to_NESbool(direction:str)->list[bool]:
    if direction == None:
        return [False, False, False]
    NES_list = []
    NES_list.append(True) if direction.find("N") != -1 else NES_list.append(False)
    NES_list.append(True) if direction.find("E") != -1 else NES_list.append(False)
    NES_list.append(True) if direction.find("S") != -1 else NES_list.append(False)
    return NES_list

def NESbool_to_NEESE(NES:list[bool])->str:
    strans = []
    if NES[0]:
        strans.append("NE")
    if NES[1]:
        strans.append("E") 
    if NES[2]:
        strans.append("SE")
    return ",".join(strans)

def N_CWbool_to_direction_symbol(N_CW:list[bool])->str:
    strans = []
    if N_CW[0]:
        strans.append("NE")
    if N_CW[1]:
        strans.append("E") 
    if N_CW[2]:
        strans.append("SE")
    if N_CW[3]:
        strans.append("SW")
    if N_CW[4]:
        strans.append("W") 
    if N_CW[5]:
        strans.append("NW")
    return ",".join(strans)

def border_state_N_CW_bool(border_matrix:list[list[str]], pos_square:rw.frame.Coordinate)->list[bool]:
    border_now = str_to_NESbool(border_matrix[pos_square.x()][pos_square.y()])
    border_NW = str_to_NESbool(border_matrix[pos_square.x()][pos_square.y() + 1])
    border_W = str_to_NESbool(border_matrix[pos_square.x() - 1][pos_square.y()])
    border_SW = str_to_NESbool(border_matrix[pos_square.x() - 1][pos_square.y() - 1])
    return border_now + [border_SW[0], border_W[1], border_NW[2]]
