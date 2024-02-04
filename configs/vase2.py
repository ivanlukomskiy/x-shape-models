import math
import os

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform, round_mesh_points, save_stl
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 35
config.height = 140
config.thickness = 3
config.base_cell_height = 28
config.base_cell_width = 28
config.frame_len_bottom = 3
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: 1

shape = generate_cylindrical_shape(config)


def warp_vase_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    scale = 1 + z / config.height * 0.4
    angle = angle + z / config.height * 3.7
    return from_cylindrical_coords(angle, distance * scale, z)


transform = warp_vase_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)
shape = round_mesh_points(shape, 3)
save_stl(shape, os.path.splitext(os.path.basename(__file__))[0])

