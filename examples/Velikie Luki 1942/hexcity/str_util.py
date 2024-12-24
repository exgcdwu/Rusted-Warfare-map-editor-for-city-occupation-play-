def get_str_end_split(instr:str, tag:str)->list:
    instr_temp = instr.split(tag)
    if len(instr_temp) > 1:
        end_str = instr_temp[-1]
        origin_str = "".join(instr_temp[:-1])
    else:
        end_str = ""
        origin_str = "".join(instr_temp)
    return [origin_str, end_str]