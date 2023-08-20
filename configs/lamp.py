import math

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform
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
config.cell_fullness_function = lambda angle, h_fraction: max(min(h_fraction, 1), 0)

shape = generate_cylindrical_shape(config)


def warp_lamp_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    scale = 1 - 2.2 * math.pow(max(abs((z - config.frame_len_bottom) / config.height_without_frame - 0.35), 0), 3) + 0.3
    return from_cylindrical_coords(angle, distance * scale, z)


transform = warp_lamp_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)

shape.save('lamp.stl')