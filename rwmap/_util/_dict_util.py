
def dict_isconflict(a:dict, b:dict)->None:
    for an, av in a.items():
        if b.get(an) != None and av != b[an]:
            return True
    return False
