from src.config import SpiralShapeConfig
from src.mesh_utils import round_mesh_points
from src.spiral import generate_spiral_shape

config = SpiralShapeConfig()
config.radius = 100
config.height = 160
config.thickness = 0.6
config.base_cell_height = 6
config.base_cell_width = 3.5
config.frame_len_bottom = 3
config.frame_len_top = 3
config.length = 1100
config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 or h_fraction == 0 else 0

shape = generate_spiral_shape(config)
shape = round_mesh_points(shape, 3)
shape.save('roll_small.stl')
