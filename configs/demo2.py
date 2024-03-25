import os

import numpy as np

from src.mesh_utils import save_stl, join_meshes
from src.x_shape import create_x_shape

shapes = []
for j in range(2):
    for i in range(3):
        shape = create_x_shape(10, 3, 14, 0, 0, 0.3, 0.3)
        shape.translate(np.array([i * 10,0,  j * 14]))
        shapes.append(shape)

mesh = join_meshes(*shapes)

save_stl(mesh, os.path.splitext(os.path.basename(__file__))[0])
