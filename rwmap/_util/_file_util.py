import os

def combine_path(current_dir:str, target_path:str)->str:
    current_dir = os.path.abspath(current_dir)
    
    if not os.path.isabs(target_path):
        target_path = os.path.join(current_dir, target_path)
        target_path = os.path.abspath(target_path)
    
    return target_path

def find_file(current_dir:str, target_path:str)->str:
    target_path = combine_path(current_dir, target_path)
    
    if os.path.exists(target_path):
        return target_path
    else:
        return None
    
def get_path(path_now:str, path_original:str, path_target:str)->str:
    if os.path.isabs(path_target):
        return path_target
    else:
        abs_path_target = os.path.join(os.path.dirname(path_original), path_target)
        return os.path.relpath(abs_path_target, os.path.dirname(path_now))