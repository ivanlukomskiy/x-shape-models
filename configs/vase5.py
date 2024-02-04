import math
import os

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform, round_mesh_points, save_stl
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 38
config.height = 170
config.thickness = 3.5
config.base_cell_height = 3
config.base_cell_width = 3
config.frame_len_bottom = 3
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: 1

shape = generate_cylindrical_shape(config)

vertical_ribs = 20
horizontal_rivs = 130


def warp_vase_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    z_fraction = max(min(z / config.height, 1), 0)

    phase = 1 + math.sin(angle * vertical_ribs + z_fraction * horizontal_rivs) / 2
    scale = 1 + math.sin(math.pi * pow(z_fraction, 0.8) - math.pi / 5) / 6
    if distance > config.radius:
        scale += phase / 8 * math.sin(math.pi * z_fraction)
    return from_cylindrical_coords(angle, distance * scale, z)


transform = warp_vase_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)
shape = round_mesh_points(shape, 3)
save_stl(shape, os.path.splitext(os.path.basename(__file__))[0])
