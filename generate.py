import os.path

import yaml
import argparse

from src.mesh_utils import round_mesh_points, default_precision
from src.pattern_circular import circular_array
from src.pattern_spherical import spherical_array
from src.pattern_spiral import spiral_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='X shape models generator')
    parser.add_argument('config', type=str, help='name of the config file from "configs" to use (w/o extension)')
    args = parser.parse_args()

    file = os.path.join('configs', f'{args.config}.yaml')
    with open(file) as stream:
        config = yaml.safe_load(stream)
        if config['pattern'] == 'circular':
            res = circular_array(config)
        elif config['pattern'] == 'spherical':
            res = spherical_array(config)
        elif config['pattern'] == 'spiral':
            res = spiral_array(config)
        else:
            raise RuntimeError('Unsupported pattern ' + config['pattern'])

        res = round_mesh_points(res, default_precision)

        res.save(f'{args.config}.stl')

