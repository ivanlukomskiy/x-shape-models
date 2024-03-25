import os

from src.config import FlatShapeConfig
from src.mesh_utils import save_stl
from src.shape_flat import generate_flat_shape

config = FlatShapeConfig()
config.width = 100
config.height = 110
config.base_cell_width = 5
config.base_cell_height = 5
config.frame_len_bottom = 5
config.frame_len_top = 5

mesh = generate_flat_shape(config)

save_stl(mesh, os.path.splitext(os.path.basename(__file__))[0])
