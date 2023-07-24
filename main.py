import math

import numpy as np
from stl import mesh

filename='net.stl'
width = 2
height = 3
line = 0.42
middle_line_h = 0.6
middle_line_v = 0.6
thickness = 0.42
v_cells = 13
h_cells = 11
frame_thickness = 10
frame_width = 2


def rotate_points_around_z(points, angle_degrees):
    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)

    # Define the rotation matrix for Z-axis
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    rotation_matrix = np.array([[cos_theta, -sin_theta, 0],
                                [sin_theta, cos_theta, 0],
                                [0, 0, 1]])

    # Perform the rotation on all points
    rotated_points = np.dot(points, rotation_matrix.T)

    return rotated_points


def add_square(arr, a, b, c, d, invert):
    if not invert:
        arr.extend([
            [a, b, d],
            [d, b, c]
        ])
    else:
        arr.extend([
            [a, d, b],
            [d, c, b]
        ])


def add_triangle(arr, a, b, c, invert):
    if not invert:
        arr.extend([
            [a, b, c],
        ])
    else:
        arr.extend([
            [a, c, b],
        ])


def draw_leg(rotation, shift, scale):
    vertices = (np.array([
        [0, 0, 0],
        [0, middle_line_v / 2, 0],
        [width / 2 - middle_line_h / 2, height / 2, 0],
        [width / 2, height / 2, 0],
        [width / 2, height / 2 - middle_line_v / 2, 0],
        [middle_line_h / 2, 0, 0],
        [0, 0, -thickness],
        [0, middle_line_v / 2, -thickness],
        [width / 2 - middle_line_h / 2, height / 2, -thickness],
        [width / 2, height / 2, -thickness],
        [width / 2, height / 2 - middle_line_v / 2, -thickness],
        [middle_line_h / 2, 0, -thickness],
    ]) + np.array(shift)) * np.array(scale)
    vertices = rotate_points_around_z(vertices, rotation)
    faces = []

    invert = scale[0] * scale[1] * scale[2] < 0

    add_square(faces, 1, 2, 8, 7, invert)
    add_square(faces, 11, 7, 8, 10, invert)
    add_square(faces, 2, 1, 5, 4, invert)
    add_square(faces, 10, 4, 5, 11, invert)
    add_triangle(faces, 8, 9, 10, invert)
    add_triangle(faces, 6, 7, 11, invert)
    add_triangle(faces, 4, 3, 2, invert)
    add_triangle(faces, 1, 0, 5, invert)

    faces = np.array(faces)
    leg = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            leg.vectors[i][j] = vertices[f[j], :]
    return leg


def combine_meshes(*meshes):
    return mesh.Mesh(np.concatenate([m.data for m in meshes]))


def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)
    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)


def array(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, 0, col, 'x')
                if row != 0:
                    translate(_copy, l, 0, row, 'y')
                if layer != 0:
                    translate(_copy, h, 0, layer, 'z')
                copies.append(_copy)
    return copies


def frame_patch(rotation, shift, scale, width, height):
    vertices = (np.array([
        [width / 2 - middle_line_h / 2, -height, 0],
        [-width / 2 + middle_line_h / 2, -height, 0],
        [width / 2 - middle_line_h / 2, -height, -thickness],
        [-width / 2 + middle_line_h / 2, -height, -thickness],
        [width / 2, -height, 0],
        [-width / 2, -height, 0],
        [width / 2, -height, -thickness],
        [-width / 2, -height, -thickness],
        [width / 2, -height, 0 + (frame_thickness - thickness) / 2],
        [-width / 2, -height, 0 + (frame_thickness - thickness) / 2],
        [width / 2, -height, -thickness - (frame_thickness - thickness) / 2],
        [-width / 2, -height, -thickness - (frame_thickness - thickness) / 2],
    ]) + np.array(shift) + np.array([-width / 2, 0, 0])) * np.array(scale)
    vertices = rotate_points_around_z(vertices, rotation)
    faces = []
    invert = scale[0] * scale[1] * scale[2] < 0
    add_square(faces, 0, 2, 3, 1, invert)
    add_square(faces, 10, 11, 7, 6, invert)
    add_square(faces, 4, 5, 9, 8, invert)
    faces = np.array(faces)
    leg = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            leg.vectors[i][j] = vertices[f[j], :]
    return leg


def frame_ext(width, thickness, shift, rotation, scale):
    vertices = (np.array([
        [0, 0, 0],
        [width, 0, 0],
        [width + frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, 0],
        [- frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, 0],
        [0, 0, -thickness],
        [width, 0, -thickness],
        [width + frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, -thickness],
        [- frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, -thickness],
    ]) + np.array(shift)) * np.array(scale)
    vertices = rotate_points_around_z(vertices, rotation)
    faces = []
    invert = scale[0] * scale[1] * scale[2] < 0
    add_triangle(faces, 0, 2, 1, invert)
    add_triangle(faces, 0, 3, 2, invert)
    add_triangle(faces, 4, 5, 6, invert)
    add_triangle(faces, 4, 6, 7, invert)
    add_square(faces, 2, 3, 7, 6, invert)
    faces = np.array(faces)
    leg = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            leg.vectors[i][j] = vertices[f[j], :]
    return leg


def cap(shift, scale, rotation, thickness, width):
    vertices = (np.array([
        [0, 0, 0],
        [width, 0, 0],
        [width + frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, 0],
        [- frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, 0],
        [0, 0, -thickness],
        [width, 0, -thickness],
        [width + frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, -thickness],
        [- frame_width * math.cos(math.pi / 4), -math.cos(math.pi / 4) * frame_width, -thickness],
    ]) + np.array(shift)) * np.array(scale)
    vertices = rotate_points_around_z(vertices, rotation)
    faces = []
    invert = scale[0] * scale[1] * scale[2] < 0
    add_square(faces, 4, 0, 3, 7, invert)
    add_square(faces, 5, 6, 2, 1, invert)
    faces = np.array(faces)
    leg = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            leg.vectors[i][j] = vertices[f[j], :]
    return leg


def cap_patch(rotation, shift, scale, width):
    vertices = (np.array([
        [width / 2 - middle_line_h / 2, 0, 0],
        [-width / 2 + middle_line_h / 2, 0, 0],
        [width / 2 - middle_line_h / 2, 0, -thickness],
        [-width / 2 + middle_line_h / 2, 0, -thickness],
        [width / 2, 0, 0],
        [-width / 2, 0, 0],
        [width / 2, 0, -thickness],
        [-width / 2, 0, -thickness],
        # [width / 2, -height, 0 + (frame_thickness - thickness) / 2],
        # [-width / 2, -height, 0 + (frame_thickness - thickness) / 2],
        # [width / 2, -height, -thickness - (frame_thickness - thickness) / 2],
        # [-width / 2, -height, -thickness - (frame_thickness - thickness) / 2],
    ]) + np.array(shift) + np.array([-width / 2, 0, 0])) * np.array(scale)
    vertices = rotate_points_around_z(vertices, rotation)
    faces = []
    invert = scale[0] * scale[1] * scale[2] < 0
    add_square(faces, 0, 4, 6, 2, invert)
    add_square(faces, 1, 3, 7, 5, invert)
    # add_square(faces, 4, 5, 9, 8, invert)
    faces = np.array(faces)
    leg = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            leg.vectors[i][j] = vertices[f[j], :]
    return leg


def frame():
    patch1 = frame_patch(0, 0, [1, 1, 1], width, height)
    # patch2 = frame_patch(180, [-width * (h_cells - 2), -height * (v_cells - 2), 0], [1, 1, 1], width, height)
    patches_x_1 = array(patch1, [width, height, 0], 1, h_cells, 1)
    # patches_x_2 = array(patch2, [-width, height, 0], 1, h_cells, 1)

    patch3 = frame_patch(90, [0, -width * (h_cells - 2), 0], [1, 1, 1], height, width)
    patch4 = frame_patch(270, [-height * (v_cells - 2), 0, 0], [1, 1, 1], height, width)
    patches_x_3 = array(patch3, [width, height, height], v_cells, 1, 1)
    patches_x_4 = array(patch4, [width, -height, -height], v_cells, 1, 1)

    frame_ext_1 = frame_ext(width * h_cells, frame_thickness,
                            [-width, -height, frame_thickness / 2 - thickness / 2],
                            0, [1, 1, 1])
    # frame_ext_2 = frame_ext(width * h_cells, frame_thickness,
    #                         [-width * (h_cells - 1), -height * (v_cells - 1), frame_thickness / 2 - thickness / 2],
    #                         180, [1, 1, 1])
    frame_ext_3 = frame_ext(height * v_cells, frame_thickness,
                            [-height, -width * (h_cells - 1), frame_thickness / 2 - thickness / 2],
                            90, [1, 1, 1])
    frame_ext_4 = frame_ext(height * v_cells, frame_thickness,
                            [-height * (v_cells - 1), -width, frame_thickness / 2 - thickness / 2],
                            270, [1, 1, 1])

    c = cap([-width * (h_cells - 1), -height * (v_cells - 1), frame_thickness / 2 - thickness / 2], [1, 1, 1], 180, frame_thickness, width * h_cells)
    c_patch = cap_patch(180, [-width * (h_cells - 2), height * (v_cells - 1), 0], [1, -1, 1], width)
    c_patches = array(c_patch, [-width, height, 0], 1, h_cells, 1)

    return combine_meshes(patch1,
                          c,
                          c_patch,
                          *c_patches,
                          # patch2,
                          patch3, patch4, frame_ext_1,
                          # frame_ext_2,
                          frame_ext_3, frame_ext_4,
                          *patches_x_1,
                          # *patches_x_2,
                          *patches_x_3, *patches_x_4)


x1 = draw_leg(0, [-width, -height, 0], [1, 1, 1])
x2 = draw_leg(180, [0, 0, 0], [1, 1, 1])
x3 = draw_leg(0, [0, -height, 0], [-1, 1, 1])
x4 = draw_leg(180, [-width, 0, 0], [-1, 1, 1])
x = combine_meshes(x1, x2, x3, x4)
net_copies = array(x, [width, height, 0], v_cells, h_cells, 1)

res = combine_meshes(x, frame(), *net_copies)

res.save(filename)
