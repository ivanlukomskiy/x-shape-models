import math

from src.config import CircularShapeConfig
from src.mesh_utils import get_radial_transform, snap_transform_to_layers
from src.shape_circular import generate_circular_shape

config = CircularShapeConfig()
config.radius = 22
config.height = 65
config.thickness = 1.5
config.base_cell_height = 22
config.base_cell_width = 4
config.frame_len_bottom = 2
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: max(min(1 - h_fraction, 1), 0)

shape = generate_circular_shape(config)

def transform(angle, distance, z):
    return 1 + 3 * math.pow(clamp)


    return 1 + 3 * math.pow(max(abs(z / config.height) + 0.1, 0), 0.5) + 0.3

warp = lambda z, total_h: 1 + 3 * math.pow(max(abs(z / total_h) + 0.1, 0), 0.5) + 0.3,
transform = get_radial_transform(config, warp)
transform = snap_transform_to_layers(config, transform)

shape.save('bowl.stl')
