from rwmap._object import TObject_One
import rwmap._exceptions as rwexception

def add_time_pro(name:str, aint:float, issecond:bool = True)->dict[str, str]:
    if aint != -1:
        if issecond:
            if isinstance(aint, int):
                return {name: f"{str(aint)}s"}
            else:
                return {name: f"{aint:.2f}s"}
        else:
            return {name: str(int(aint))}
    else:
        return {}
    
def add_str_pro(name:str, value:str)->dict[str, str]:
    if value != None:
        return {name:str(value)}
    else:
        return {}
    
def add_acti_pro(name:str, tob_list:list[TObject_One])->dict[str, str]:
    value_list = []
    if tob_list != []:
        for tobject in tob_list:
            value_list.append(tobject._name)
            if tobject._name == None:
                raise rwexception.ObjectNameError\
            ("The object does not have a name but participates in activation or deactivation.")
        value_list = list(set(value_list))
        value = ",".join(value_list)
        return {name: value}
    else:
        return {}