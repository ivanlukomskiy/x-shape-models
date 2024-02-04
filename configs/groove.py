import math
import os

from src.groove import create_groove_segment
from src.mesh_utils import round_mesh_points, save_stl

shape = create_groove_segment(30, 10, 40, 3, 1, 1, 4, -5, math.pi / 4, 0)

shape = round_mesh_points(shape, 3)
save_stl(shape, os.path.splitext(os.path.basename(__file__))[0])
