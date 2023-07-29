import math

import numpy as np

from mesh_utils import combine_meshes, get_noise, noise
from x_shape import x_shape


def circular_array(
        r, d, h, n_horizontal, n_vertical, contact_fraction_h, contact_fraction_v, frame_len
):
    angle_step = 2 * math.pi / n_horizontal
    truncation_angle = angle_step / 2
    l_shape = 2 * r * math.sin(truncation_angle)
    center_distance = r * math.cos(truncation_angle)
    bricks = []
    l = math.pi * 2 * r / 7

    for j in range(n_vertical):
        for i in range(n_horizontal):
            fullness = [
                get_noise(noise, l * math.sin(i * angle_step), h * (j + .5)),
                get_noise(noise, l * math.sin((i - 0.5) * angle_step), h * j),
                get_noise(noise, l * math.sin(i * angle_step), h * (j - .5)),
                get_noise(noise, l * math.sin((i + 0.5) * angle_step), h * j),
            ]
            brick = x_shape(
                l_shape, d, h,
                truncation_angle,
                -truncation_angle,
                contact_fraction_h, contact_fraction_v,
                frame_top=j == n_vertical - 1,
                frame_bottom=j == 0,
                frame_len=frame_len,
                fullness=fullness
            )
            brick.translate(np.array([0, center_distance, h * j]))
            brick.rotate(np.array([0, 0, 1]), angle_step * i)
            bricks.append(brick)


    return combine_meshes(*bricks)
