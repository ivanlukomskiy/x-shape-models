import math

import numpy as np

from src.mesh_utils import join_meshes
from src.x_shape import create_x_shape


fullness_functions = {
    'linear': lambda angle, h_fraction: max(min(h_fraction, 1), 0),
    'zeros': lambda angle, h_fraction: 0,
    'glass': lambda angle, h_fraction: .1 if h_fraction > 0.87 else 0,
    'by_the_frame': lambda angle, h_fraction: 1 if h_fraction == 1 else 0,
}


def screw_function(h_fraction):
    return h_fraction


def circular_shape(config):
    radius = config['radius']
    x_width = config['x_width']
    n_horizontal = round(math.pi * 2 * radius / x_width)
    x_height = config['x_height']
    n_vertical = round(config['height'] / x_height)
    thickness = config['thickness']
    contact_fraction_h = config['contact_fraction_h']
    contact_fraction_v = config['contact_fraction_v']
    frame_len_top = config.get('frame_len_top', config.get('frame_len'))
    frame_len_bottom = config.get('frame_len_bottom', config.get('frame_len'))

    fullness_func_name = config.get('fullness_function', 'zeros')
    fullness_func = fullness_functions[fullness_func_name]

    angle_step = 2 * math.pi / n_horizontal
    truncation_angle = angle_step / 2
    l_shape = 2 * radius * math.sin(truncation_angle)
    center_distance = radius * math.cos(truncation_angle)
    bricks = []

    for j in range(n_vertical):
        for i in range(n_horizontal):
            fullness = [
                fullness_func(i * angle_step, (j + 1) / n_vertical),
                fullness_func((i - 0.5) * angle_step, (j+0.5) / n_vertical),
                fullness_func(i * angle_step, j / n_vertical),
                fullness_func((i + 0.5) * angle_step, (j+0.5) / n_vertical),
            ]
            frame_top = frame_len_top > 0 and j == n_vertical - 1
            frame_bottom = frame_len_bottom > 0 and j == 0
            cap_top = frame_len_top == 0 and j == n_vertical - 1
            cap_bottom = frame_len_bottom == 0 and j == 0
            bottom = config.get('bottom', False) and j == 0

            brick = create_x_shape(
                l_shape, thickness, x_height,
                truncation_angle,
                -truncation_angle,
                contact_fraction_h, contact_fraction_v,
                frame_top=frame_top,
                frame_bottom=frame_bottom,
                frame_len_bottom=frame_len_bottom,
                frame_len_top=frame_len_top,
                fullness=fullness,
                top_cap=cap_top,
                bottom_cap=cap_bottom,
                bottom=bottom
            )
            brick.translate(np.array([0, center_distance, x_height * j]))
            brick.rotate(np.array([0, 0, 1]), angle_step * i)
            bricks.append(brick)

    return join_meshes(*bricks)
