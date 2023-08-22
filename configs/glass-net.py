from src.config import CircularShapeConfig
from src.mesh_utils import round_mesh_points
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 30
config.height = 91
config.thickness = 12
config.base_cell_height = 5
config.base_cell_width = 5
config.frame_len_bottom = 14
config.frame_len_top = 2
config.bottom = True
config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 else 0

shape = generate_cylindrical_shape(config)
shape = round_mesh_points(shape, 3)
shape.save('glass-net.stl')
