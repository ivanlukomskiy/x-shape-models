import math

import numpy as np

from mesh_utils import square, triangle, build_mesh


def x_shape(truncation_angle_1, truncation_angle_2, contact_fraction_h, contact_fraction_v):
    pass


def _x_shape_quarter(truncation_angle, contact_fraction_h, contact_fraction_v, top_cap=False, bottom_cap=False,
                     top_patch=False, bottom_patch=False):
    x_delta = math.tan(truncation_angle) / 2
    vertices = np.array([
        [1 - x_delta, -0.5, 0],
        [0, -0.5, 1 - contact_fraction_v],
        [0, -0.5, 1],
        [contact_fraction_h, -0.5, 1],
        [1 + x_delta, -0.5, contact_fraction_v],
        [1 + x_delta, 0.5, 1 - contact_fraction_v],
        [0, 0.5, 0],
        [0, 0.5, 1],
        [contact_fraction_h, 0.5, 1],
        [1 + x_delta, 0.5, contact_fraction_v],
        [1 - x_delta - contact_fraction_h, -0.5, 0],
        [1 - x_delta - contact_fraction_h, 0.5, 0],
        [1 - x_delta, -0.5, 1],
        [1 + x_delta, 0.5, 1],
        [0, -0.5, 0],
        [0, 0.5, 0],
    ])
    faces = [
        *square(10, 1, 3, 4),
        *triangle(1, 2, 3),
        *triangle(10, 4, 0),

        *square(5, 11, 8, 7),
        *triangle(6, 5, 7),
        *triangle(8, 11, 9),

        *square(1, 10, 11, 5),
        *square(8, 4, 3, 7),
    ]
    print(faces)
    if top_cap:
        faces.extend(square(7, 6, 3, 2))
    if bottom_cap:
        faces.extend(square(0, 10, 11, 9))
    if top_patch:
        faces.extend(square(12, 3, 7, 13))
    if bottom_patch:
        faces.extend(square(10, 14, 15, 11))

    return build_mesh(faces, vertices)
