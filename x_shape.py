import math

import numpy as np

from mesh_utils import square, triangle, build_mesh, combine_meshes


def x_shape(
        l, d, h,
        truncation_angle_1,
        truncation_angle_2,
        contact_fraction_h,
        contact_fraction_v,
        bottom_cap=False,
        top_cap=False,
        frame_top=False,
        frame_bottom=False,
        frame_len=0,
        left_cap=False,
        right_cap=False,
        fullness=None,
):
    if fullness is None:
        fullness = [0, 0, 0, 0]
    # its 0.6 0.6 0.6 0.6
    mesh1 = _x_shape_quarter(l / 2, d, h / 2, truncation_angle_1, contact_fraction_h, contact_fraction_v,
                             bottom_cap=bottom_cap, frame=frame_bottom, frame_len=frame_len, bottom_patch=frame_bottom,
                             side_cap=right_cap,
                             fullness_a=min(fullness[3] * 2, 1),
                             # fullness_b=0.1)
                             fullness_b=-max(fullness[2] * 2 - 1, 0),
                             a_cap=fullness[3] <= 0.5, trace=True)
    mesh2 = _x_shape_quarter(l / 2, d, -h / 2, truncation_angle_1, contact_fraction_h, contact_fraction_v,
                             bottom_cap=top_cap, frame=frame_top, frame_len=-frame_len, bottom_patch=frame_top,
                             side_cap=right_cap,
                             fullness_a=-max(fullness[3] * 2 - 1, 0),
                             fullness_b=min(fullness[0] * 2, 1),
                             b_cap=fullness[0] <= 0.5)
    mesh2.translate(np.array([0, 0, h]))
    mesh3 = _x_shape_quarter(-l / 2, d, h / 2, truncation_angle_2, contact_fraction_h, contact_fraction_v,
                             bottom_cap=bottom_cap, frame=frame_bottom, frame_len=frame_len, bottom_patch=frame_bottom,
                             side_cap=left_cap,
                             fullness_a=min(fullness[1] * 2, 1),
                             fullness_b=-max(fullness[2] * 2 - 1, 0),
                             a_cap=fullness[1] <= 0.5)
    mesh4 = _x_shape_quarter(-l / 2, d, -h / 2, truncation_angle_2, contact_fraction_h, contact_fraction_v,
                             bottom_cap=top_cap, frame=frame_top, frame_len=-frame_len, bottom_patch=frame_top,
                             side_cap=left_cap,
                             fullness_a=-max(fullness[1] * 2 - 1, 0),
                             fullness_b=min(fullness[0] * 2, 1),
                             b_cap=fullness[0] <= 0.5)
    mesh4.translate(np.array([0, 0, h]))
    return combine_meshes(
        mesh1,
        mesh2,
        mesh3,
        mesh4
    )


def _x_shape_quarter(
        l, d, h,
        truncation_angle,
        contact_fraction_h,
        contact_fraction_v,
        fullness_a=0,
        fullness_b=0,
        a_cap=False,
        b_cap=False,
        bottom_cap=False,
        bottom_patch=False,
        side_cap=False,
        frame=False,
        frame_len=0,
        trace=False,
):
    delta_x = math.tan(truncation_angle) * d / 2
    contact_h = contact_fraction_h * l
    contact_v = contact_fraction_v * h

    if fullness_a > 0:
        h_a = contact_v + (h - contact_v) * fullness_a
        shift_a = 1-math.fabs(fullness_a)
    else:
        h_a = contact_v + (h - contact_v) * (1 - math.fabs(fullness_a))
        shift_a = math.fabs(fullness_a)

    if fullness_b > 0:
        shift_b = math.fabs(fullness_b)
        h_b = (h - contact_v) * (1 - math.fabs(fullness_b))  # == 0
    else:
        shift_b = 1-math.fabs(fullness_b)
        h_b = (h - contact_v) * (math.fabs(fullness_b))  # == 0

    vertices = np.array([
        [l - delta_x, -0.5 * d, 0],  # 0
        [0, -0.5 * d, h - contact_v],  # 1
        [0, -0.5 * d, h],  # 2
        [contact_h, -0.5 * d, h],  # 3
        [l - delta_x, -0.5 * d, contact_v],  # 4
        [0, 0.5 * d, h - contact_v],  # 5
        [0, 0.5 * d, h],  # 6
        [contact_h, 0.5 * d, h],  # 7
        [l + delta_x, 0.5 * d, contact_v],  # 8
        [l + delta_x, 0.5 * d, 0],  # 9
        [l - delta_x - contact_h, -0.5 * d, 0],  # 10
        [l - contact_h, 0.5 * d, 0],  # 11
        [l - delta_x, -0.5 * d, h],  # 12
        [l + delta_x, 0.5 * d, h],  # 13
        [0, -0.5 * d, 0],  # 14
        [0, 0.5 * d, 0],  # 15
        [l - delta_x, -0.5 * d, -frame_len],  # 16
        [0, -0.5 * d, -frame_len],  # 17
        [0, 0.5 * d, -frame_len],  # 18
        [l + delta_x, 0.5 * d, -frame_len],  # 19

        [contact_h + (l - delta_x - contact_h) * shift_a, -0.5 * d, h_a],  # 20
        [l - delta_x, -0.5 * d, h_a],  # 21
        [l + delta_x, 0.5 * d, h_a],  # 22
        [contact_h + (l + delta_x - contact_h) * shift_a, 0.5 * d, h_a],  # 23

        [(l - delta_x - contact_h) * shift_b, -0.5 * d, h_b],  # 24
        [0, -0.5 * d, h_b],  # 25
        [0, 0.5 * d, h_b],  # 26
        [(l - delta_x - contact_h) * shift_b, 0.5 * d, h_b],  # 27
    ])
    inverse = h * l * d < 0
    faces = [
        # left side
        *square(3, 1, 10, 4, inverse),
        *triangle(1, 3, 2, inverse),
        *triangle(10, 0, 4, inverse),

        # right side
        *square(5, 7, 8, 11, inverse),
        *triangle(6, 7, 5, inverse),
        *triangle(8, 9, 11, inverse),
    ]

    # upper surface
    if fullness_a == 0:
        faces.extend(square(8, 7, 3, 4, inverse))
    elif fullness_a > 0:
        if fullness_a < 1:
            faces.extend(square(23, 7, 3, 20, inverse))
        if a_cap:
            faces.extend(square(23, 20, 21, 22, inverse))
        faces.extend(triangle(8, 23, 22, inverse))
        faces.extend(triangle(4, 21, 20, inverse))
    else:
        faces.extend(square(22, 21, 20, 23, inverse))
        faces.extend(square(8, 23, 20, 4, inverse))
        # sides
        faces.extend(square(7, 13, 22, 23, inverse))
        faces.extend(square(12, 3, 20, 21, inverse))

    # fixme prevent cap on full b-fullness
    if fullness_b == 0:
        faces.extend(square(1, 5, 11, 10, inverse))
    elif fullness_b > 0:
        if b_cap:
            faces.extend(square(25, 26, 27, 24, inverse))
        if fullness_b < 1:
            faces.extend(square(24, 27, 11, 10, inverse))
        faces.extend(triangle(5, 27, 26, inverse))
        faces.extend(triangle(1, 25, 24, inverse))
    else:
        faces.extend(square(1, 5, 27, 24, inverse))
        faces.extend(square(27, 26, 25, 24, inverse))
        # sides
        faces.extend(square(27, 11, 15, 26, inverse))
        faces.extend(square(25, 14, 10, 24, inverse))

    if side_cap:
        if frame:
            faces.extend(square(0, 16, 19, 9, inverse))
        if fullness_a > 0:
            faces.extend(square(21, 0, 9, 22, inverse))
        elif fullness_a < 0:
            faces.extend(square(4, 0, 9, 8, inverse))
            faces.extend(square(12, 21, 22, 13, inverse))
        else:
            faces.extend(square(4, 0, 9, 8, inverse))

    if bottom_cap:
        faces.extend(square(0, 10, 11, 9, inverse))

    if bottom_patch and fullness_b >= 0:
        faces.extend(square(10, 11, 15, 14, inverse))

    if frame:
        faces.extend(square(0, 14, 17, 16, inverse))
        faces.extend(square(15, 9, 19, 18, inverse))
        faces.extend(square(16, 17, 18, 19, inverse))

    return build_mesh(faces, vertices)
