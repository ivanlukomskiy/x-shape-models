import math

import numpy as np
from stl import mesh

from circular import circular_array


def get_scale_at_edge(z, total_h):
    return 1 - 2.2 * math.pow(max(abs(z / total_h - 0.35), 0), 3) + 0.3


def transform(x, y, z, h, total_h):
    # if z % h < 0.0001:
    #     scale = get_scale_at_edge(z, total_h)
    #     return x * scale, y * scale, z

    prev_edge = math.floor(z / h) * h
    next_edge = prev_edge + h

    scale = (get_scale_at_edge(prev_edge, total_h) * (next_edge - z) / h +
             get_scale_at_edge(next_edge, total_h) * (z - prev_edge) / h)
    return x * scale, y * scale, z


def spherical_array(
        r, d, h, n_horizontal, n_vertical, contact_fraction_h, contact_fraction_v, frame_len
):
    circular = circular_array(r, d, h, n_horizontal, n_vertical, contact_fraction_h, contact_fraction_v, frame_len)
    res = mesh.Mesh(np.zeros(circular.data.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(circular.points):
        transformed = []
        for j in range(3):
            transformed.extend(transform(f[j * 3], f[j * 3 + 1], f[j * 3 + 2], h, h * n_vertical))
        res.points[i] = np.array(transformed)
    return res
