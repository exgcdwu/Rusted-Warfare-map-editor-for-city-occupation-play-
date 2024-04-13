import rwmap._frame as frame
import rwmap._tile as tile

import rwmap.data.tile_group_grid._tile_group_matrix as tile_matrix
import rwmap.data.tile_group_grid._tile_group_addlayer as tile_addlayer

ft_water_dict = {"ft": frame.TagCoordinate.init_xy("Deep Water")}

fill_tile_group_one_ground_water_28_24 = tile.TileGroup_One.init_tilegroup_addlayer(
    ft_water_dict, tile_addlayer.fill_tile_group_addlayer_ground_28_24
)