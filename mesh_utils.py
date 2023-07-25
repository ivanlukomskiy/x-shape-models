import numpy as np
from stl import mesh


def square(a, b, c, d):
    return [
        [a, b, d],
        [d, b, c]
    ]


def triangle(a, b, c):
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
