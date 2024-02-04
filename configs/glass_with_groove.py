import os

import numpy as np

from src.config import CircularShapeConfig
from src.mesh_utils import round_mesh_points, join_meshes, save_stl
from src.shape_circular import generate_cylindrical_shape

radius = 30
thickness = 12
base_cell_height = 5
base_cell_width = 5
total_height = 105
groove_height = 25
bottom_part_height = 65

bottom_part_config = CircularShapeConfig()
bottom_part_config.radius = radius
bottom_part_config.height = bottom_part_height
bottom_part_config.thickness = thickness
bottom_part_config.base_cell_height = base_cell_height
bottom_part_config.base_cell_width = base_cell_width
bottom_part_config.frame_len_bottom = 14
bottom_part_config.bottom = True
bottom_part_config.open_top = True
bottom_part_config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 else 0
bottom_part = generate_cylindrical_shape(bottom_part_config)


def get_x_shape_transform(stretch_bottom, stretch_top, center_distance, height):
    def transform(x, y, z):
        if y < 0:  # inner surface
            return x, y, z

        z_share = z / height
        stretch = stretch_bottom * (1 - z_share) + stretch_top * z_share

        y = (y + center_distance) * stretch - center_distance
        x = x * stretch

        return x, y, z
    return transform


def generate_groove_segment(z_current, height, stretch_bottom, stretch_top):
    segment = CircularShapeConfig()
    segment.radius = radius
    segment.height = height
    segment.thickness = thickness
    segment.base_cell_height = height
    segment.base_cell_width = base_cell_width
    segment.open_bottom = True
    segment.open_top = True
    segment.cell_fullness_function = lambda angle, h_fraction: 1
    segment.x_shape_transform = get_x_shape_transform(stretch_bottom, stretch_top, segment.center_distance, segment.height)
    mesh = generate_cylindrical_shape(segment)
    mesh.translate(np.array([0, 0, z_current]))
    return z_current + height, mesh


chamfer_height_small = .5
chamfer_height_large = 2
ring_height = 2
cavity_height = groove_height - chamfer_height_large * 2 - chamfer_height_small * 2 - ring_height * 2

ring_stretch = (radius + .5) / radius
cavity_stretch = (radius - 1) / radius

meshes = [bottom_part]
z = bottom_part_config.height
z, mesh = generate_groove_segment(z, chamfer_height_small, 1, ring_stretch)
meshes.append(mesh)
z, mesh = generate_groove_segment(z, ring_height, ring_stretch, ring_stretch)
meshes.append(mesh)
z, mesh = generate_groove_segment(z, chamfer_height_large, ring_stretch, cavity_stretch)
meshes.append(mesh)
z, mesh = generate_groove_segment(z, cavity_height, cavity_stretch, cavity_stretch)
meshes.append(mesh)
z, mesh = generate_groove_segment(z, chamfer_height_large, cavity_stretch, ring_stretch)
meshes.append(mesh)
z, mesh = generate_groove_segment(z, ring_height, ring_stretch, ring_stretch)
meshes.append(mesh)
z, mesh = generate_groove_segment(z, chamfer_height_small, ring_stretch, 1)
meshes.append(mesh)

top_part_config = CircularShapeConfig()
top_part_config.radius = radius
top_part_config.height = total_height - groove_height - bottom_part_height
top_part_config.thickness = thickness
top_part_config.base_cell_height = base_cell_height
top_part_config.base_cell_width = base_cell_width
top_part_config.frame_len_top = 2
top_part_config.open_bottom = True
top_part_config.cell_fullness_function = lambda angle, h_fraction: 1 if h_fraction == 1 or h_fraction == 0 else 0
top_part = generate_cylindrical_shape(top_part_config)
top_part.translate(np.array([0, 0, z]))
meshes.append(top_part)

glass = join_meshes(*meshes)
glass = round_mesh_points(glass, 3)
save_stl(glass, os.path.splitext(os.path.basename(__file__))[0])
