import math

from src.config import CircularShapeConfig
from src.mesh_utils import snap_transform_to_layers, to_cylindrical_coords, \
    from_cylindrical_coords, apply_transform
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 60
config.height = 193
config.thickness = 18
config.base_cell_height = 50
config.base_cell_width = 40
config.frame_len_bottom = 3
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: 0.1 if h_fraction == 1 else 0

shape = generate_cylindrical_shape(config)


def warp_vase_transform(x, y, z):
    angle, distance, z = to_cylindrical_coords(x, y, z)
    scale = 1 + z / config.height * 0.4
    angle = angle + z / config.height * 3.7
    return from_cylindrical_coords(angle, distance * scale, z)


transform = warp_vase_transform
transform = snap_transform_to_layers(config, transform)
shape = apply_transform(shape, transform)

shape.save('vase.stl')

'''
pattern: spherical
radius: 50
height: 190
thickness: 18
x_height: 50
x_width: 40
contact_fraction_h: 0.3
contact_fraction_v: 0.3
frame_len_top: 0
frame_len_bottom: 2
fullness_function: glass
warp_function: vase
bottom: true
screw_function: vase
'''
