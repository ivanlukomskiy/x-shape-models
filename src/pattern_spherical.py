import math

from src.mesh_utils import radial_transform_mesh
from src.pattern_circular import circular_array

warp_functions = {
    'lamp': lambda z, total_h:  1 - 2.2 * math.pow(max(abs(z / total_h - 0.35), 0), 3) + 0.3,
    'bowl': lambda z, total_h:  1 + 3 * math.pow(max(abs(z / total_h) + 0.1, 0), 0.5) + 0.3,
    'saddle': lambda z, total_h:  1 + 1.6 * math.pow(max(abs(z / total_h - 0.35), 0), 3) + 0.3,
    'glass': lambda z, total_h:  1 + z/total_h * 0.2,
}


def spherical_array(config):
    x_height = config['x_height']
    n_vertical = round(config['height'] / x_height)

    circular = circular_array(config)

    # bend cylinder by moving its points horizontally toward its axis
    warp_function_name = config.get('warp_function', 'lamp')
    warp_function = warp_functions[warp_function_name]
    return radial_transform_mesh(circular, x_height, n_vertical, warp_function)
