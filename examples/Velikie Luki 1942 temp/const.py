import os
_current_dir_path = os.path.dirname(os.path.abspath(__file__))
_example_dir_path = os.path.dirname(_current_dir_path)

_map_process_dir = "map_process"
_map_storage_dir = "map_storage"
_template = "template"
basic_data = "basic_data"
terrain = "terrain"
tile_group = "tile_group"
river = "river"

template_dir_path = _example_dir_path + "\\" + _template
map_process_dir_path = _current_dir_path + "\\" + _map_process_dir
map_storage_dir_path = _current_dir_path + "\\" + _map_storage_dir
basic_data_path = _current_dir_path + "\\" + basic_data
terrain_path = _current_dir_path + "\\" + terrain
tile_group_path = _current_dir_path + "\\" + tile_group
river_path = _current_dir_path + "\\" + river