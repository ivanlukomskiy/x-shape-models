import math

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform, round_mesh_points
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 90
config.height = 229
config.thickness = 1
config.base_cell_height = 12
config.base_cell_width = 7
config.frame_len_bottom = 6
config.frame_len_top = 6
config.bottom = True

def fullness(angle, h_fraction):
    return max(min((h_fraction - config.frame_len_bottom / config.height) * 1.1, 1), 0)


config.cell_fullness_function = fullness

shape = generate_cylindrical_shape(config)


def warp_lamp_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    scale = 1 - 2.2 * math.pow(max(abs((z - config.frame_len_bottom) / config.height_without_frame - 0.35), 0), 3) + 0.3
    return from_cylindrical_coords(angle, distance * scale, z)


transform = warp_lamp_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)
shape = round_mesh_points(shape, 3)
shape.save('lamp.stl')
