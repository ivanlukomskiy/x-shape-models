import math
import os
import random

from src.config import SpiralShapeConfig
from src.mesh_utils import round_mesh_points, save_stl
from src.shape_spiral import generate_spiral_shape

config = SpiralShapeConfig()
config.radius = 25
config.height = 100
config.thickness = 5
config.base_cell_height = 20
config.base_cell_width = 16
config.length = 60
config.roll_layers_gap = 60

def fullness(angle, h_fraction):
    return min(max(h_fraction*1.2 - 0.1, 0), 1)

config.cell_fullness_function = fullness

shape = generate_spiral_shape(config)
shape = round_mesh_points(shape, 3)
save_stl(shape, os.path.splitext(os.path.basename(__file__))[0])
