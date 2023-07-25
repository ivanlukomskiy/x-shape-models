import math

import numpy as np

from mesh_utils import combine_meshes
from x_shape import x_shape


def get_coords(r0, a, angle):
    return (
        (a * angle + r0) * math.cos(angle),
        (a * angle + r0) * math.sin(angle),
    )


def spiral_array(
        r0, a, d, h, step_angle, n_horizontal, n_vertical, contact_fraction_h, contact_fraction_v, frame_len
):
    current_angle = 0
    r_prev = r0
    x_prev, y_prev = get_coords(r0, a, current_angle)

    bricks = []

    for j in range(n_vertical):
        for i in range(n_horizontal):
            current_angle += step_angle
            x1, y1 = get_coords(r0, a, current_angle)
            r1 = a * current_angle + r0
            length = math.hypot(x1 - x_prev, y1 - y_prev)
            k = 2 * r_prev * math.sin(step_angle / 2)
            delta_r = r1 - r_prev

            truncate_angle_1 = math.acos((length ** 2 + k ** 2 - delta_r ** 2) / (2 * length * k)) - step_angle / 2
            truncate_angle_2 = math.pi / 2 - math.acos((length ** 2 + delta_r ** 2 - k ** 2) / (2 * length * delta_r))
            # truncate_angle_1 = math.acos((length ** 2 + k ** 2 - delta_r ** 2) / (2 * length * k))
            # truncate_angle_2 = math.pi / 2 - math.acos((length ** 2 - k ** 2 + delta_r ** 2) / (2 * length * delta_r))
            truncate_angle_1 = -truncate_angle_1
            truncate_angle_2 = -truncate_angle_2

            print(truncate_angle_1, truncate_angle_2)
            x_mid = (x1 + x_prev) / 2
            y_mid = (y1 + y_prev) / 2
            norm_angle = - math.atan2(y1 - y_prev, x1 - x_prev)

            brick = x_shape(
                length, d, h,
                # 0,0,
                truncate_angle_2,
                truncate_angle_1,
                contact_fraction_h, contact_fraction_v,
                frame_top=j == n_vertical - 1,
                frame_bottom=j == 0,
                frame_len=frame_len
            )
            brick.rotate(np.array([0, 0, 1]), norm_angle)
            brick.translate(np.array([x_mid, y_mid, h * j]))
            # brick.rotate(np.array([0, 0, 1]), current_angle - step_angle)
            bricks.append(brick)

            x_prev, y_prev, r_prev = x1, y1, r1

    return combine_meshes(*bricks)
