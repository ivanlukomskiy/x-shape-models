import math

import numpy as np

from mesh_utils import combine_meshes
from x_shape import x_shape


def circular_array(
        r, d, h, n_horizontal, n_vertical, contact_fraction_h, contact_fraction_v,
):
    angle_step = 2 * math.pi / n_horizontal
    truncation_angle = angle_step / 2
    l_shape = 2 * r * math.sin(truncation_angle)
    center_distance = r * math.cos(truncation_angle)
    bricks = []
    for i in range(n_horizontal):
        # r = 10
        # trunc angle ok
        # l_shape ok
        # center_distance ok

        print(l_shape, d, h, math.degrees(truncation_angle), center_distance)
        brick = x_shape(
            l_shape, d, h / 2,
            truncation_angle,
            truncation_angle,
            contact_fraction_h, contact_fraction_v,
        )
        brick.translate(np.array([0, center_distance, 0]))
        brick.rotate(np.array([0, 0, 1]), angle_step * i)
        bricks.append(brick)

    return combine_meshes(*bricks)