from src.config import SpiralShapeConfig
from src.mesh_utils import round_mesh_points
from src.shape_spiral import generate_spiral_shape

config = SpiralShapeConfig()
config.radius = 25
config.height = 46
config.thickness = 5
config.base_cell_height = 20
config.base_cell_width = 16
config.frame_len_bottom = 4
config.frame_len_top = 4
config.length = 380
config.roll_layers_gap = 10
config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 or h_fraction == 0 else 0

shape = generate_spiral_shape(config)
shape = round_mesh_points(shape, 3)
shape.save('roll_demo.stl')
