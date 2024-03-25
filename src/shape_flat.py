import math

import numpy as np

from src.config import FlatShapeConfig
from src.mesh_utils import join_meshes
from src.x_shape import create_x_shape


def generate_flat_shape(config: FlatShapeConfig):
    x_shapes = []

    for layer in range(config.layers_count):
        for i in range(config.layers_x_shapes_count):
            frame_top = layer == config.layers_count - 1
            frame_bottom = layer == 0
            shape = create_x_shape(
                config.cell_width,
                config.thickness,
                config.cell_height,
                0,
                0,
                config.contact_fraction_h,
                config.contact_fraction_v,
                frame_top=frame_top,
                frame_bottom=frame_bottom,
                frame_len_top=config.frame_len_top,
                frame_len_bottom=config.frame_len_bottom,
                left_cap=i == 0,
                right_cap=i == config.layers_x_shapes_count - 1,
            )
            shape.translate(np.array([i * config.cell_width, 0, layer * config.cell_height]))
            x_shapes.append(shape)

    joint_mesh = join_meshes(*x_shapes)
    joint_mesh.translate(np.array([0, 0, config.frame_len_bottom]))
    return joint_mesh
