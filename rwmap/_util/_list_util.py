from copy import deepcopy

import rwmap._frame as frame

def fill_list_of_list(element, size:frame.Coordinate):
    return [[deepcopy(element)] * size.x() for i in range(size.y())]

def list_variable_s(element_s):
    if isinstance(element_s, list):
        return element_s
    elif element_s == None:
        return element_s
    else:
        return [element_s]
    
def list_get_s(list_s:list, index:int):
    if index < len(list_s):
        return list_s[index]
    else:
        return None
    
def team_list_inv(team_num:int, team_list:list[int])->list[int]:
    team_listn = [True] * team_num
    for team in team_list:
        team_listn[team] = False
    team_inv = []
    for team, isteam_inv in enumerate(team_listn):
        if isteam_inv == True:
            team_inv.append(team)
    return team_inv

def search_list_to_index(nlist:list, value)->int:
    try:
        return nlist.index(value)
    except ValueError:
        return -1
    
def list_filling(nlist:list, length:int, value, istolist = False)->list:
    nlist_now = [[deepcopy(value)] if istolist else deepcopy(value) for value in nlist] + [deepcopy(value) for i in range(length - len(nlist))]
    return nlist_now

def remove_nth_occurrence(lst:list, value, n:int):
    indices = [i for i, x in enumerate(lst) if x == value]
    if len(indices) >= n + 1:
        del lst[indices[n]]