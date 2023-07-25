import math

import numpy as np

from mesh_utils import square, triangle, build_mesh


def x_shape(truncation_angle_1, truncation_angle_2, contact_fraction_h, contact_fraction_v):
    pass


def _x_shape_quarter(truncation_angle, contact_fraction_h, contact_fraction_v, top_cap=False, bottom_cap=False,
                     top_patch=False, bottom_patch=False, right_cap=False, right_patch=False, left_cap=False,
                     left_patch=False):
    x_delta = math.tan(truncation_angle) / 2
    vertices = np.array([
        [1 - x_delta, -0.5, 0],
        [0, -0.5, 1 - contact_fraction_v],
        [0, -0.5, 1],
        [contact_fraction_h, -0.5, 1],
        [1 - x_delta, -0.5, contact_fraction_v],
        [0, 0.5, 1 - contact_fraction_v],
        [0, 0.5, 1],  # 6
        [contact_fraction_h, 0.5, 1],  # 7
        [1 + x_delta, 0.5, contact_fraction_v],  # 8
        [1 + x_delta, 0.5, 0],  # 9
        [1 - x_delta - contact_fraction_h, -0.5, 0],  # 10
        [1 - contact_fraction_h, 0.5, 0],  # 11
        [1 - x_delta, -0.5, 1],
        [1 + x_delta, 0.5, 1],
        [0, -0.5, 0],  # 14
        [0, 0.5, 0],  # 15
    ])
    faces = [
        *square(3, 1, 10, 4),
        *triangle(1, 3, 2),
        *triangle(10, 0, 4),

        *square(5, 7, 8, 11),
        *triangle(6, 7, 5),
        *triangle(8, 9, 11),

        *square(1, 5, 11, 10),
        *square(8, 7, 3, 4),
    ]
    if top_cap:
        faces.extend(square(7, 6, 2, 3))
    if bottom_cap:
        faces.extend(square(0, 10, 11, 9))
    if top_patch:
        faces.extend(square(12, 3, 7, 13))
    if bottom_patch:
        faces.extend(square(10, 11, 15, 14))
    if left_cap:
        faces.extend(square(1,2,6,5))
    if right_cap:
        faces.extend(square(4,0,9,8))
    if right_patch:
        faces.extend(square(4,12,13,8))
    if left_patch:
        faces.extend(square(1,14,15,5))

    return build_mesh(faces, vertices)
