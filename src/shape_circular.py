import math

import numpy as np

from src.config import CircularShapeConfig
from src.mesh_utils import join_meshes
from src.x_shape import create_x_shape


def generate_cylindrical_shape(config: CircularShapeConfig):
    truncation_angle = config.cell_center_angle / 2
    x_shape_width = 2 * config.radius * math.sin(truncation_angle)
    center_distance = config.radius * math.cos(truncation_angle)

    x_shapes = []

    for layer in range(config.layers_count):
        for i in range(config.layer_cells_count):
            fullness = [
                config.cell_fullness_function(i * config.cell_center_angle,
                                              (layer + 1) / config.layers_count),
                config.cell_fullness_function((i - 0.5) * config.cell_center_angle,
                                              (layer + 0.5) / config.layers_count),
                config.cell_fullness_function(i * config.cell_center_angle,
                                              layer / config.layers_count),
                config.cell_fullness_function((i + 0.5) * config.cell_center_angle,
                                              (layer + 0.5) / config.layers_count),
            ]
            frame_top = config.frame_len_top > 0 and layer == config.layers_count - 1
            frame_bottom = config.frame_len_bottom > 0 and layer == 0
            cap_top = config.frame_len_top == 0 and layer == config.layers_count - 1 and not config.open_top
            cap_bottom = config.frame_len_bottom == 0 and layer == 0 and not config.open_bottom


            x_shape = create_x_shape(
                x_shape_width,
                config.thickness,
                config.cell_height,
                truncation_angle,
                -truncation_angle,
                config.contact_fraction_h,
                config.contact_fraction_v,
                frame_top=frame_top,
                frame_bottom=frame_bottom,
                frame_len_top=config.frame_len_top,
                frame_len_bottom=config.frame_len_bottom,
                fullness=fullness,
                top_cap=cap_top,
                bottom_cap=cap_bottom,
                bottom=config.bottom
            )
            x_shape.translate(np.array([0, center_distance, config.cell_height * layer + config.frame_len_bottom]))
            x_shape.rotate(np.array([0, 0, 1]), config.cell_center_angle * i)
            x_shapes.append(x_shape)

    joint_mesh = join_meshes(*x_shapes)
    joint_mesh.translate(np.array([0, 0, config.frame_len_bottom]))
    return joint_mesh

