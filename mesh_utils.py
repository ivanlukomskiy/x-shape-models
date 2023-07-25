import numpy as np
from stl import mesh


def square(a, b, c, d, inverse=False):
    if inverse:
        return [
            [a, d, b],
            [d, c, b]
        ]
    else:
        return [
            [a, b, d],
            [d, b, c]
        ]


def triangle(a, b, c, inverse=False):
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


def combine_meshes(*meshes):
    return mesh.Mesh(np.concatenate([m.data for m in meshes]))
