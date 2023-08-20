from src.config import CircularShapeConfig
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 32.5
config.height = 91
config.thickness = 12
config.base_cell_height = 5
config.base_cell_width = 5
config.frame_len_bottom = 14
config.frame_len_top = 2
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 else 0

shape = generate_cylindrical_shape(config)
shape.save('glass-net.stl')
