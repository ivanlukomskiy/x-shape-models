from src.config import SpiralShapeConfig
from src.spiral import generate_spiral_shape

config = SpiralShapeConfig()
config.radius = 100
config.height = 220
config.thickness = 0.6
config.base_cell_height = 6
config.base_cell_width = 3.5
config.frame_len_bottom = 3
config.frame_len_top = 3
config.length = 1010
config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 else 0

shape = generate_spiral_shape(config)

shape.save('roll_large.stl')