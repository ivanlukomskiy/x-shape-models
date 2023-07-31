import math

from src.mesh_utils import round_mesh_points, default_precision, radial_transform_mesh
from src.pattern_circular import circular_array


def get_scale(z, total_h):
    return 1 - 2.2 * math.pow(max(abs(z / total_h - 0.35), 0), 3) + 0.3


def spherical_array(config):
    x_height = config['x_height']
    n_vertical = round(config['height'] / x_height)

    circular = circular_array(config)

    # bend cylinder by moving its points horizontally toward its axis
    return radial_transform_mesh(circular, x_height, n_vertical, get_scale)
