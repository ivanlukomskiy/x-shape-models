import math

import numpy as np
from stl import mesh

from src.config import BaseConfig

default_precision = 3


def square(a, b, c, d, inverse=False):
    return [
        *triangle(a, b, d, inverse),
        *triangle(d, b, c, inverse),
    ]


def triangle(a, b, c, inverse=False):
    if a == b or b == c or c == a:
        return []
    if inverse:
        return [
            [a, c, b],
        ]
    else:
        return [
            [a, b, c],
        ]


def build_mesh(faces, vertices):
    faces = np.array(faces)
    res = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            res.vectors[i][j] = vertices[f[j], :]
    return res


def join_meshes(*meshes):
    return mesh.Mesh(np.concatenate([m.data for m in meshes]))


# mesh points positions should be rounded to avoid floating point imprecision resulting in non-manifold edges
def round_mesh_points(mesh_, precision):
    res = mesh.Mesh(np.zeros(mesh_.data.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(mesh_.points):
        res.points[i] = np.zeros(9)
        for j in range(9):
            res.points[i][j] = round(f[j], precision)
    return res


def radial_translate_point(x, y, z, h, full_height, radial_multiplier_func, screw_function):
    prev_edge_z = math.floor(z / h) * h
    next_edge_z = prev_edge_z + h
    scale = (radial_multiplier_func(prev_edge_z, full_height) * (next_edge_z - z) / h +
             radial_multiplier_func(next_edge_z, full_height) * (z - prev_edge_z) / h)
    x, y = x * scale, y * scale
    rotation_angle = (screw_function(prev_edge_z / h) * (next_edge_z - z) / h +
                      screw_function(next_edge_z / h) * (z - prev_edge_z) / h)
    x_new = x * math.cos(rotation_angle) - y * math.sin(rotation_angle)
    y_new = x * math.sin(rotation_angle) + y * math.cos(rotation_angle)
    return x_new, y_new, z


def radial_transform_mesh(mesh_, h, n_vertical, radial_multiplier_func, screw_function):
    res = mesh.Mesh(np.zeros(mesh_.data.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(mesh_.points):
        transformed = []
        for j in range(3):
            transformed.extend(radial_translate_point(f[j * 3], f[j * 3 + 1], f[j * 3 + 2], h, h * n_vertical,
                                                      radial_multiplier_func, screw_function))
        res.points[i] = np.array(transformed)
    return res


def snap_transform_to_layers(config: BaseConfig, transform):
    def translate_point(x, y, z):
        prev_layer_index = math.floor((z - config.frame_len_bottom) / config.cell_height)
        prev_layer_z = prev_layer_index * config.cell_height + config.frame_len_bottom
        next_layer_z = prev_layer_z + config.cell_height

        x_prev, y_prev, z_prev = transform(x, y, prev_layer_z)
        x_next, y_next, z_next = transform(x, y, next_layer_z)

        next_fraction = (z - prev_layer_z) / config.cell_height
        prev_fraction = (next_layer_z - z) / config.cell_height

        return (
            x_prev * prev_fraction + x_next * next_fraction,
            y_prev * prev_fraction + y_next * next_fraction,
            z,
        )

    return translate_point


def get_radial_transform(config: BaseConfig, radial_scale_func):
    def translate_point(x, y, z):
        angle = math.atan2(y, x)
        z_fraction = z / config.height
        return radial_scale_func(angle, z_fraction) * x, radial_scale_func(angle, z_fraction) * y, z

    return translate_point


def to_cylindrical_coords(x, y, z):
    angle = math.atan2(y, x)
    distance = math.hypot(x, y)
    return angle, distance, z


def from_cylindrical_coords(angle, distance, z):
    x = math.cos(angle) * distance
    y = math.sin(angle) * distance
    return x, y, z


def apply_transform(_mesh, transform):
    res = mesh.Mesh(np.zeros(_mesh.data.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(_mesh.points):
        transformed = []
        for j in range(3):
            transformed.extend(transform(f[j * 3], f[j * 3 + 1], f[j * 3 + 2]))
        res.points[i] = np.array(transformed)
    return res
