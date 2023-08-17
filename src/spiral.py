import math

import numpy as np

from src.mesh_utils import combine_meshes
from src.x_shape import x_shape


def get_spiral_point(r0, a, angle):
    return (
        (a * angle + r0) * math.cos(angle),
        (a * angle + r0) * math.sin(angle),
    )


def spiral_shape(config):
    r0 = config['spiral_initial_radius']
    a = config['spiral_layers_gap']
    d = config['thickness']
    x_height = config['x_height']
    x_width = config['x_width']
    height = config['height']
    total_length = config['spiral_length']
    contact_fraction_h = config['contact_fraction_h']
    contact_fraction_v = config['contact_fraction_v']
    frame_len = config['frame_len']

    step_angle = x_width / r0
    height_without_frame = height - frame_len * 2
    n_vertical = round(height_without_frame / x_height)
    x_height = height_without_frame / n_vertical

    current_angle = 0
    current_length = 0
    r_prev = r0
    x_prev, y_prev = get_spiral_point(r0, a, current_angle)

    bricks = []
    truncation_angles = []

    segments_count = 0
    while current_length < total_length:
        segments_count += 1
        current_angle += step_angle
        x1, y1 = get_spiral_point(r0, a, current_angle)
        r1 = a * current_angle + r0
        length = math.hypot(x1 - x_prev, y1 - y_prev)
        current_length += length
        k = 2 * r_prev * math.sin(step_angle / 2)
        delta_r = r1 - r_prev
        truncate_angle_2 = -math.pi / 2 + math.acos((length ** 2 + delta_r ** 2 - k ** 2) / (2 * length * delta_r))
        truncate_angle_1 = -math.acos((length ** 2 + k ** 2 - delta_r ** 2) / (2 * length * k)) + step_angle / 2
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

    for j in range(n_vertical):
        current_angle = 0
        current_length = 0
        x_prev, y_prev = get_spiral_point(r0, a, current_angle)
        for i in range(segments_count):
            current_angle += step_angle
            x1, y1 = get_spiral_point(r0, a, current_angle)
            r1 = a * current_angle + r0
            length = math.hypot(x1 - x_prev, y1 - y_prev)
            current_length += length

            truncate_angle_2 = truncation_angles[i][0]
            truncate_angle_1 = truncation_angles[i][1]

            x_mid = (x1 + x_prev) / 2
            y_mid = (y1 + y_prev) / 2
            norm_angle = - math.atan2(y1 - y_prev, x1 - x_prev)

            fullness = [
                1 if j == n_vertical - 1 else 0,
                0,
                1 if j == 0 else 0,
                0
            ]
            frame_top = frame_len > 0 and j == n_vertical - 1
            frame_bottom = frame_len > 0 and j == 0
            cap_top = frame_len == 0 and j == n_vertical - 1
            cap_bottom = frame_len == 0 and j == 0
            brick = x_shape(
                length, d, x_height,
                truncate_angle_1,
                truncate_angle_2,
                contact_fraction_h, contact_fraction_v,
                frame_top=frame_top,
                frame_bottom=frame_bottom,
                frame_len_top=frame_len,
                frame_len_bottom=frame_len,
                top_cap=cap_top,
                bottom_cap=cap_bottom,
                left_cap=i == 0,
                right_cap=i == segments_count - 1,
                fullness=fullness,
            )
            brick.rotate(np.array([0, 0, 1]), norm_angle)
            brick.translate(np.array([x_mid, y_mid, x_height * j * 1.]))
            bricks.append(brick)

            x_prev, y_prev, r_prev = x1, y1, r1

    return combine_meshes(*bricks)
