import math

import numpy as np

from src.mesh_utils import combine_meshes
from src.x_shape import x_shape


def get_fullness(angle, h_fraction):
    return max(min(h_fraction * 1.15, 1), 0)


def circular_array(config):
    radius = config['radius']
    x_width = config['x_width']
    n_horizontal = round(math.pi * 2 * radius / x_width)
    x_height = config['x_height']
    n_vertical = round(config['height'] / x_height)
    thickness = config['thickness']
    contact_fraction_h = config['contact_fraction_h']
    contact_fraction_v = config['contact_fraction_v']
    frame_len = config['frame_len']

    angle_step = 2 * math.pi / n_horizontal
    truncation_angle = angle_step / 2
    l_shape = 2 * radius * math.sin(truncation_angle)
    center_distance = radius * math.cos(truncation_angle)
    bricks = []

    for j in range(n_vertical):
        for i in range(n_horizontal):
            fullness = [
                get_fullness(i * angle_step, (j + .5) / n_vertical),
                get_fullness((i - 0.5) * angle_step, j / n_vertical),
                get_fullness(i * angle_step, (j - .5) / n_vertical),
                get_fullness((i + 0.5) * angle_step, j / n_vertical),
            ]
            frame_top = frame_len > 0 and j == n_vertical - 1
            frame_bottom = frame_len > 0 and j == 0
            cap_top = frame_len == 0 and j == n_vertical - 1
            cap_bottom = frame_len == 0 and j == 0

            brick = x_shape(
                l_shape, thickness, x_height,
                truncation_angle,
                -truncation_angle,
                contact_fraction_h, contact_fraction_v,
                frame_top=frame_top,
                frame_bottom=frame_bottom,
                frame_len=frame_len,
                fullness=fullness,
                top_cap=cap_top,
                bottom_cap=cap_bottom,
            )
            brick.translate(np.array([0, center_distance, x_height * j]))
            brick.rotate(np.array([0, 0, 1]), angle_step * i)
            bricks.append(brick)

    return combine_meshes(*bricks)
