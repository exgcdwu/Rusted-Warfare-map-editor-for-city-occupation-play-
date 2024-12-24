import rwmap as rw
import tile_group_1.tile_group_matrix as tile_matrix

tile_group_addlayer_ground_hex28_32_fill = \
rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    tile_matrix.tile_group_hex28_32_fill
)

tile_group_addlayer_ground_hex28_32_fill_light_barrier = \
rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    tile_matrix.tile_group_hex28_32_light_barrier
)

tile_group_addlayer_ground_hex28_32_fill_barrier_terrain = \
rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    tile_matrix.tile_group_hex28_32_barrier_terrain
)

tile_group_addlayer_ground_hex28_32_border = \
rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    tile_matrix.tile_group_hex28_32_border
)

tile_group_addlayer_ground_hex28_32_line = \
rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    tile_matrix.tile_group_hex28_32_line
)

tile_group_addlayer_item_hex28_32_railway = \
rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
    rw.const.NAME.Items, 
    tile_matrix.tile_group_hex28_32_railway
)

