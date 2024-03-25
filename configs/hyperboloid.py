import math
import os

import numpy as np

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform, round_mesh_points, save_stl
from src.shape_circular import generate_cylindrical_shape

# x^2/a^2 + y^2/b^2 - z^2/c^2 = 1
# given a == b:
# (x^2 + y^2) = (1 + z^2 / c^2) * a^2
# distance of a point from main axis:
# dist = sqrt(x^2 + y^2) = sqrt((1 + z^2 / c^2) * a^2) = a * sqrt(1 + z^2 / c^2)

a = 20.
c = 30.

config = CircularShapeConfig()
config.radius = 50
config.height = 100
config.thickness = 5
config.base_cell_height = 3
config.base_cell_width = 3
config.frame_len_bottom = 3
config.frame_len_top = 3
config.cell_fullness_function = lambda angle, h_fraction: 1
shape = generate_cylindrical_shape(config)

shape.translate(np.array([0, 0, -config.height / 2]))


def hyperboloid_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    hyperbolic_point_distance = a * math.sqrt(1 + z**2 / c**2)
    target_distance = (distance - config.radius) + hyperbolic_point_distance
    return from_cylindrical_coords(angle, target_distance, z)


transform = hyperboloid_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)
shape = round_mesh_points(shape, 3)
save_stl(shape, os.path.splitext(os.path.basename(__file__))[0])
