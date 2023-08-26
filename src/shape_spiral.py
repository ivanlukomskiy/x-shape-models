import math

import numpy as np

from src.config import SpiralShapeConfig
from src.mesh_utils import join_meshes
from src.x_shape import create_x_shape


def generate_spiral_shape(config: SpiralShapeConfig):
    current_angle = 0
    current_length = 0
    r_prev = config.radius
    x_prev, y_prev = config.get_point(current_angle)

    x_shapes = []
    truncation_angles = []

    # 1. precalculate truncation angles (angle at which adjacent x-shapes join)

    segments_count = 0
    while current_length < config.length:
        step_angle = config.get_center_angle(current_angle)
        segments_count += 1
        current_angle += step_angle
        x1, y1 = config.get_point(current_angle)
        r1 = config.get_radius(current_angle)
        x_shape_width = math.hypot(x1 - x_prev, y1 - y_prev)
        current_length += x_shape_width
        k = 2 * r_prev * math.sin(step_angle / 2)
        delta_r = r1 - r_prev
        truncate_angle_2 = -math.pi / 2 + math.acos(
            (x_shape_width ** 2 + delta_r ** 2 - k ** 2) / (2 * x_shape_width * delta_r))
        truncate_angle_1 = -math.acos(
            (x_shape_width ** 2 + k ** 2 - delta_r ** 2) / (2 * x_shape_width * k)) + step_angle / 2
        truncation_angles.append([truncate_angle_1, truncate_angle_2])
        x_prev, y_prev, r_prev = x1, y1, r1

    for i in range(len(truncation_angles)):
        current = truncation_angles[i]
        if i == 0:
            current[0] = 0
        if i == len(truncation_angles) - 1:
            current[1] = 0
            break
        next = truncation_angles[i + 1]
        avg = -(current[1] + next[0]) / 2
        current[1] += avg
        next[0] += avg

    # 2. fill the shape

    for layer in range(config.layers_count):
        current_angle = 0
        current_length = 0
        x_prev, y_prev = config.get_point(current_angle)
        for i in range(segments_count):
            step_angle = config.get_center_angle(current_angle)
            current_angle += step_angle
            x1, y1 = config.get_point(current_angle)
            r1 = config.get_radius(current_angle)
            x_shape_width = math.hypot(x1 - x_prev, y1 - y_prev)
            current_length += x_shape_width

            truncate_angle_2 = truncation_angles[i][0]
            truncate_angle_1 = truncation_angles[i][1]

            x_mid = (x1 + x_prev) / 2
            y_mid = (y1 + y_prev) / 2
            norm_angle = - math.atan2(y1 - y_prev, x1 - x_prev)

            fullness = [
                config.cell_fullness_function(current_angle, (layer + 1) / config.layers_count),
                config.cell_fullness_function(current_angle + step_angle / 2, (layer + .5) / config.layers_count),
                config.cell_fullness_function(current_angle, layer / config.layers_count),
                config.cell_fullness_function(current_angle - step_angle / 2, (layer + .5) / config.layers_count),
            ]

            frame_top = config.frame_len_top > 0 and layer == config.layers_count - 1
            frame_bottom = config.frame_len_bottom > 0 and layer == 0
            cap_top = config.frame_len_top == 0 and layer == config.layers_count - 1
            cap_bottom = config.frame_len_bottom == 0 and layer == 0
            x_shape = create_x_shape(
                x_shape_width,
                config.thickness,
                config.cell_height,
                truncate_angle_1,
                truncate_angle_2,
                config.contact_fraction_h,
                config.contact_fraction_v,
                frame_top=frame_top,
                frame_bottom=frame_bottom,
                frame_len_top=config.frame_len_top,
                frame_len_bottom=config.frame_len_bottom,
                top_cap=cap_top,
                bottom_cap=cap_bottom,
                left_cap=i == 0,
                right_cap=i == segments_count - 1,
                fullness=fullness,
            )
            x_shape.rotate(np.array([0, 0, 1]), norm_angle)
            x_shape.translate(np.array([x_mid, y_mid, config.cell_height * layer * 1.]))
            x_shapes.append(x_shape)

            x_prev, y_prev, r_prev = x1, y1, r1

    return join_meshes(*x_shapes)
