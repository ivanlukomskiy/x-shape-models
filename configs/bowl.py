import math

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 22
config.height = 65
config.thickness = 1.5
config.base_cell_height = 22
config.base_cell_width = 4
config.frame_len_bottom = 2
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: max(min(1 - h_fraction, 1), 0)

shape = generate_cylindrical_shape(config)


def warp_bowl_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    scale = 1 + 3 * math.pow(max(abs(z / config.height) + 0.1, 0), 0.5) + 0.3
    return from_cylindrical_coords(angle, distance * scale, z)


transform = warp_bowl_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)

shape.save('bowl.stl')
