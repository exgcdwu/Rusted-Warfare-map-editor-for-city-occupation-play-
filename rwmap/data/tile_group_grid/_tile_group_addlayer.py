import rwmap.data.default_data as const
import rwmap._tile as tile

import rwmap.data.tile_group_grid._tile_group_matrix as tile_matrix

fill_tile_group_addlayer_ground_28_24 = \
tile.TileGroup_AddLayer.init_tilegroup_matrix(const.GROUND_LAYER_STR, tile_matrix.fill_tile_group_matrix28_24)