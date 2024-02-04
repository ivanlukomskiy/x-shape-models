from src.config import CircularShapeConfig
from src.mesh_utils import round_mesh_points, save_stl
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 15
config.height = 18
config.thickness = 10
config.base_cell_height = 18
config.base_cell_width = 10

shape = generate_cylindrical_shape(config)
shape = round_mesh_points(shape, 3)
save_stl(shape, 'toy.stl')

