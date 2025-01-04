BRACEMAXCHAR = 100
BRACEMAXLEVEL = 2
BNUM = 1
MAXLEVEL = 1

def config_element_str_line(config_element, level, max_level):
    if level > max_level:
        return ""

    element = config_element[0]

    str_ans = ""
    if isinstance(element, dict):
        str_ans = str_ans + '{'
        for key, value in element.items():
            str_ans = str_ans + f"{key}: " + \
                config_element_str_line(value, level + 1, max_level) + ', '
        str_ans = str_ans[0:-2] + '}'
    elif isinstance(element, list):
        str_ans = str_ans + '['
        for item in element:
            str_ans = str_ans + config_element_str_line(item, level + 1, max_level) + ', '
        str_ans = str_ans[0:-2] + ']'
    else:
        str_ans = str_ans + f"{element}"
    return str_ans

def config_element_str_now(config_element, level, max_level, onum, bnum , bracemaxlevel, bracemaxchar):
    if level > max_level:
        return ""
    
    element = config_element[0]

    str_ans = ""
    if isinstance(element, dict):
        str_ans = str_ans + " " * onum + '{\n'
        for key, value in element.items():
            if level + bracemaxlevel >= max_level and value[1] < bracemaxchar:
                    str_add = " " * (bnum + onum) + f"{key}: {config_element_str_line(value, level + 1, max_level)}\n"
            else:
                str_add = " " * (bnum + onum) + f"{key}: \n" + \
                    config_element_str_now(value, level + 1, max_level, onum + bnum + len(key) + 2, bnum)
                    
            str_ans = str_ans + str_add

        str_ans = str_ans + " " * onum + '}\n'
    elif isinstance(element, list):
        str_ans = str_ans + " " * onum + '[\n'
        for item in element:
            if level + bracemaxlevel >= max_level and item[1] < bracemaxchar:
                str_add = " " * (bnum + onum) + f"{config_element_str_line(item, level + 1, max_level)}\n"
            else:
                str_add = config_element_str_now(item, level + 1, max_level, onum + bnum, bnum)
            str_ans = str_ans + str_add
        str_ans = str_ans + " " * onum + ']\n'
    else:
        str_ans = str_ans + " " * onum + f"{element}\n"
    return str_ans

def config_element_mark(element, level, max_level)->int:
    if level > max_level:
        return 1
    
    str_len = 4
    if isinstance(element, dict):
        for key, value in element.items():
            lene = config_element_mark(value, level + 1, max_level)
            element[key] = (value, lene)
            str_len = str_len + lene + len(key) + 4
        return str_len
    elif isinstance(element, list):
        for i, item in enumerate(element):
            lene = config_element_mark(item, level + 1, max_level)
            element[i] = (item, lene)
            str_len = str_len + lene + 2
        return str_len
    else:
        return len(str(element))

def config_element_str_t(element, max_level = MAXLEVEL, bnum = BNUM, bracemaxlevel = BRACEMAXLEVEL, bracemaxchar = BRACEMAXCHAR):
    from copy import deepcopy
    config_element = deepcopy(element)
    config_element = (config_element, config_element_mark(config_element, 0, max_level))

    if bracemaxlevel >= max_level and config_element[1] < bracemaxchar:
        return (config_element_str_line(config_element, 0, max_level), False)
    else:
        return (config_element_str_now(config_element, 0, max_level, 0, bnum, bracemaxlevel, bracemaxchar), True)
    
def config_element_str(element, max_level = MAXLEVEL, bnum = BNUM, bracemaxlevel = BRACEMAXLEVEL, bracemaxchar = BRACEMAXCHAR):
    return config_element_str_t(element, max_level = max_level, bnum = bnum, bracemaxlevel = bracemaxlevel, bracemaxchar = bracemaxchar)[0]

def config_element_str_n(element, max_level = MAXLEVEL, bnum = BNUM, bracemaxlevel = BRACEMAXLEVEL, bracemaxchar = BRACEMAXCHAR):
    config_element_str_t_ans, isenter = config_element_str_t(element, max_level = max_level, bnum = bnum, bracemaxlevel = bracemaxlevel, bracemaxchar = bracemaxchar)
    return ('\n' if isenter else '') + config_element_str_t_ans + ('\n' if isenter else '')

def print_config(element, max_level = MAXLEVEL, bnum = BNUM, bracemaxlevel = BRACEMAXLEVEL, bracemaxchar = BRACEMAXCHAR):
    print(config_element_str(element, max_level, bnum, bracemaxlevel, bracemaxchar))