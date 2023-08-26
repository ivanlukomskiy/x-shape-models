import numpy as np

from src.config import CircularShapeConfig, GrooveConfig
from src.groove import generate_groove
from src.mesh_utils import round_mesh_points, join_meshes
from src.shape_circular import generate_cylindrical_shape

radius = 30
thickness = 12
base_cell_height = 5
base_cell_width = 5
total_height = 105
groove_height = 65

# 72 => 60 => 30

bottom_part_config = CircularShapeConfig()
bottom_part_config.radius = radius
bottom_part_config.height = groove_height
bottom_part_config.thickness = thickness
bottom_part_config.base_cell_height = base_cell_height
bottom_part_config.base_cell_width = base_cell_width
bottom_part_config.frame_len_bottom = 14
bottom_part_config.bottom = True
bottom_part_config.open_top = True
bottom_part_config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 else 0
bottom_part = generate_cylindrical_shape(bottom_part_config)

groove_config = GrooveConfig()
groove_config.ring_height = 2
groove_config.chamfer1_height = .5
groove_config.chamfer2_height = 2
groove_config.ring_delta_radius = .5
groove_config.groove_delta_radius = -1
groove_config.radius = radius
groove_config.height = 25
groove_config.thickness = thickness
groove_config.base_cell_width = base_cell_width
groove_shape = generate_groove(groove_config)
groove_shape.translate(np.array([0, 0, bottom_part_config.height]))

top_part_config = CircularShapeConfig()
top_part_config.radius = radius
top_part_config.height = total_height - groove_config.height - bottom_part_config.height
top_part_config.thickness = thickness
top_part_config.base_cell_height = base_cell_height
top_part_config.base_cell_width = base_cell_width
top_part_config.frame_len_top = 2
top_part_config.open_bottom = True
top_part_config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 or h_fraction == 0 else 0
top_part = generate_cylindrical_shape(top_part_config)
top_part.translate(np.array([0, 0, bottom_part_config.height + groove_config.height]))

glass = join_meshes(bottom_part, top_part, groove_shape)
glass = round_mesh_points(glass, 3)
glass.save('glass-with-groove.stl')
