import os

import numpy as np

from src.config import FlatShapeConfig
from src.mesh_utils import save_stl, apply_transform, round_mesh_points
from src.shape_flat import generate_flat_shape

# y = (z^2 / b^2) - (x^2 / a^2)
a = 8.5
b = 8.5

config = FlatShapeConfig()
config.width = 110
config.height = 110
config.base_cell_width = 10
config.base_cell_height = 10
config.frame_len_bottom = 5
config.frame_len_top = 5
config.thickness = 5

mesh = generate_flat_shape(config)
mesh.translate(np.array([-config.width / 2, 0, -config.height / 2]))


def hyperbolic_paraboloid_transform(x, y, z):
    dy = z ** 2 / b ** 2 - x ** 2 / a ** 2
    return x, y + dy, z


mesh = apply_transform(mesh, hyperbolic_paraboloid_transform)
mesh = round_mesh_points(mesh, 3)
save_stl(mesh, os.path.splitext(os.path.basename(__file__))[0])
