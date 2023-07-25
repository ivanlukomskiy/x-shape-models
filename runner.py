import math

from circular import circular_array
from x_shape import _x_shape_quarter, x_shape

mesh = circular_array(
    10, 1, 2, 4, 10, 0.4, 0.4
)

mesh.save('viewer/wider.stl')
