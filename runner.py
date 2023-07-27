import math

from spiral import spiral_array

r = 50
avg_l_step = 3
n_horizontal = int(2 * math.pi * r / avg_l_step)
segment_height = 5
expected_height = 200
expected_length = 200
frame_len = 1
n_vertical = int((expected_height - frame_len * 2)/ segment_height)

avg_step_angle = 2 * math.pi / n_horizontal
mesh = spiral_array(
    r0=r, a=0.6, d=0.5, h=segment_height, step_angle=avg_step_angle, total_length=expected_length, n_vertical=n_vertical,
    contact_fraction_h=0.3, contact_fraction_v=0.3,
    frame_len=frame_len
)
# mesh = circular_array(
#     r=r, d=0.5, h=4, n_horizontal=n_horizontal, n_vertical=14, contact_fraction_h=0.3, contact_fraction_v=0.3,
#     frame_len=2
# )
# mesh = x_shape(1, 1, 1, math.pi / 10, math.pi / 10, 0.4, 0.4, frame_bottom=True, frame_len=2)

mesh.save('viewer/wider.stl')
