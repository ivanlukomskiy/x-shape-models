from src.config import CircularShapeConfig
from src.shape_circular import generate_cylindrical_shape

config = CircularShapeConfig()
config.radius = 15
config.height = 18
config.thickness = 10
config.base_cell_height = 18
config.base_cell_width = 10

shape = generate_cylindrical_shape(config)
shape.save('toy.stl')
