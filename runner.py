import math

from circular import circular_array
from spherical import spherical_array
from spiral import spiral_array

r = 90
avg_l_step = 7
n_horizontal = int(2 * math.pi * r / avg_l_step)
segment_height = 12
expected_height = 210
expected_length = 40
frame_len = 6
n_vertical = int((expected_height - frame_len * 2)/ segment_height)

avg_step_angle = 2 * math.pi / n_horizontal
# mesh = spiral_array(
#     r0=r, a=0.6, d=0.5, h=segment_height, step_angle=avg_step_angle, total_length=expected_length, n_vertical=n_vertical,
#     contact_fraction_h=0.3, contact_fraction_v=0.3,
#     frame_len=frame_len
# )
# mesh = circular_array(
#     r=r, d=0.5, h=4, n_horizontal=n_horizontal, n_vertical=n_vertical, contact_fraction_h=0.3, contact_fraction_v=0.3,
#     frame_len=2
# )
mesh = spherical_array(
    r=r, d=1, h=segment_height, n_horizontal=n_horizontal, n_vertical=int(expected_height/segment_height),
    contact_fraction_h=0.3, contact_fraction_v=0.3,
    frame_len=frame_len
)
# mesh = x_shape(1, 1, 1, math.pi / 10, math.pi / 10, 0.4, 0.4, frame_bottom=True, frame_len=2)

mesh.save('viewer/wider.stl')
