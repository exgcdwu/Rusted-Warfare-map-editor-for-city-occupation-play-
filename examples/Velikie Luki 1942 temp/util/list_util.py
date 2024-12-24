from copy import deepcopy

def get_listoflist_s(listoflist:list, index:list[int]):
    listnow = listoflist
    for i in range(len(index)):
        if index[i] < len(listnow):
            listnow = listnow[index[i]]
        else:
            return None
    return listnow

def list_of_list_transpose(listoflist:list[list])->list[list]:
    listoflist_ans:list[list] = [[] for i in range(len(listoflist[0]))]
    for list_n in listoflist:
        for index, ele in enumerate(list_n):
            listoflist_ans[index].append(deepcopy(ele))
    return listoflist_ans

def list_of_list_flip_vertical(listoflist:list[list])->list[list]:
    return [deepcopy(listoflist[index]) for index in range(len(listoflist) - 1, -1, -1)]

def list_of_list_flip_horizon(listoflist:list[list])->list[list]:
    listoflist_ans = []
    for listn in listoflist:
        listoflist_ans.append([deepcopy(listn[index]) for index in range(len(listn) - 1, -1, -1)])
    return listoflist_ans