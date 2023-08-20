import math

from configs.vase5 import vertical_ribs, horizontal_rivs
from src.config import SpiralShapeConfig
from src.mesh_utils import round_mesh_points, to_cylindrical_coords, from_cylindrical_coords, snap_transform_to_layers, \
    apply_transform
from src.shape_spiral import generate_spiral_shape

config = SpiralShapeConfig()
config.radius = 30
config.height = 46
config.thickness = 3
config.base_cell_height = 20
config.base_cell_width = 16
config.frame_len_bottom = 4
config.frame_len_top = 4
config.length = 300
config.roll_layers_gap = 3
config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 or h_fraction == 0 else 0

def warp_bracelet_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    distance = distance * (1 + math.sin(angle) / 1.5)
    return from_cylindrical_coords(angle, distance, z)


transform = warp_bracelet_transform
shape = generate_spiral_shape(config)
shape = apply_transform(shape, transform)
shape = round_mesh_points(shape, 3)
shape.save('bracelet.stl')
