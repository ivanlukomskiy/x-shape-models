import math

import numpy as np

from mesh_utils import square, triangle, build_mesh, combine_meshes


def x_shape(
        l, d, h,
        truncation_angle_1,
        truncation_angle_2,
        contact_fraction_h,
        contact_fraction_v,
):
    mesh1 = _x_shape_quarter(l, d, h, truncation_angle_1, contact_fraction_h, contact_fraction_v)
    mesh2 = _x_shape_quarter(l, d, -h, truncation_angle_1, contact_fraction_h, contact_fraction_v)
    mesh2.translate(np.array([0, 0, h * 2]))
    mesh3 = _x_shape_quarter(-l, d, h, truncation_angle_2, contact_fraction_h, contact_fraction_v)
    mesh4 = _x_shape_quarter(-l, d, -h, truncation_angle_2, contact_fraction_h, contact_fraction_v)
    mesh4.translate(np.array([0, 0, h * 2]))
    return combine_meshes(
        mesh1, mesh2, mesh3, mesh4
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
    print(f'truncation angle {truncation_angle}')
    x_delta = math.tan(truncation_angle) / 2
    print(f'x delta {x_delta}')

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
    scale = np.array([l, d, h])
    vertices *= scale
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
