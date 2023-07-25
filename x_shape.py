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
):
    mesh1 = _x_shape_quarter(l / 2, d, h/2 , truncation_angle_1, contact_fraction_h, contact_fraction_v, bottom_cap=bottom_cap)
    mesh2 = _x_shape_quarter(l / 2, d, -h/2, truncation_angle_1, contact_fraction_h, contact_fraction_v, bottom_cap=top_cap)
    mesh2.translate(np.array([0, 0, h]))
    mesh3 = _x_shape_quarter(-l / 2, d, h/2, truncation_angle_2, contact_fraction_h, contact_fraction_v, bottom_cap=bottom_cap)
    mesh4 = _x_shape_quarter(-l / 2, d, -h/2, truncation_angle_2, contact_fraction_h, contact_fraction_v, bottom_cap=top_cap)
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
        top_cap=False,
        bottom_cap=False,
        top_patch=False,
        bottom_patch=False,
        right_cap=False,
        right_patch=False,
        left_cap=False,
        left_patch=False
):
    x_delta = math.tan(truncation_angle) * d / 2
    contact_h = contact_fraction_h * l
    contact_v = contact_fraction_v * h

    vertices = np.array([
        [l - x_delta, -0.5 * d, 0],
        [0, -0.5 * d, h - contact_v],
        [0, -0.5 * d, h],
        [contact_h, -0.5 * d, h],
        [l - x_delta, -0.5 * d, contact_v],
        [0, 0.5 * d, h - contact_v],
        [0, 0.5 * d, h],  # 6
        [contact_h, 0.5 * d, h],  # 7
        [l + x_delta, 0.5 * d, contact_v],  # 8
        [l + x_delta, 0.5 * d, 0],  # 9
        [l - x_delta - contact_h, -0.5 * d, 0],  # 10
        [l - contact_h, 0.5 * d, 0],  # 11
        [l - x_delta, -0.5 * d, h],
        [l + x_delta, 0.5 * d, h],
        [0, -0.5 * d, 0],  # 14
        [0, 0.5 * d, 0],  # 15
    ])
    inverse = h * l * d < 0
    faces = [
        *square(3, 1, 10, 4, inverse),
        *triangle(1, 3, 2, inverse),
        *triangle(10, 0, 4, inverse),

        *square(5, 7, 8, 11, inverse),
        *triangle(6, 7, 5, inverse),
        *triangle(8, 9, 11, inverse),

        *square(1, 5, 11, 10, inverse),
        *square(8, 7, 3, 4, inverse),
    ]
    if top_cap:
        faces.extend(square(7, 6, 2, 3, inverse))
    if right_cap:
        faces.extend(square(4, 0, 9, 8, inverse))
    if bottom_cap:
        faces.extend(square(0, 10, 11, 9, inverse))
    if left_cap:
        faces.extend(square(1, 2, 6, 5, inverse))
    if top_patch:
        faces.extend(square(12, 3, 7, 13, inverse))
    if right_patch:
        faces.extend(square(4, 12, 13, 8, inverse))
    if bottom_patch:
        faces.extend(square(10, 11, 15, 14, inverse))
    if left_patch:
        faces.extend(square(1, 14, 15, 5, inverse))

    return build_mesh(faces, vertices)
