import math

from src.groove import create_groove_segment
from src.mesh_utils import round_mesh_points

groove = create_groove_segment(30, 10, 40, 3, 1, 1, 4, -5, math.pi / 4, 0)

groove = round_mesh_points(groove, 3)
groove.save('groove.stl')
