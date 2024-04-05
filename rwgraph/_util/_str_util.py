
def indentstr_Tab(str_now:str)->str:
    str_list = str_now.split("\n")
    for i in range(0, len(str_list)):
        str_list[i] = "\t" + str_list[i]
    str_list[0] = str_list[0][1:]
    str_ans = "\n".join(str_list)
    return str_ans