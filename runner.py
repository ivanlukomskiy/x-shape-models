import math

from circular import circular_array
from x_shape import _x_shape_quarter, x_shape

r = 40
avg_l_step = 1.2
n_horizontal = int(2 * math.pi * r / avg_l_step)


mesh = circular_array(
    r=r, d=0.5, h=1.4, n_horizontal=n_horizontal, n_vertical=40, contact_fraction_h=0.4, contact_fraction_v=0.4,
    frame_len=2
)
# mesh = x_shape(1, 1, 1, math.pi / 10, math.pi / 10, 0.4, 0.4, frame_bottom=True, frame_len=2)

mesh.save('viewer/wider.stl')
