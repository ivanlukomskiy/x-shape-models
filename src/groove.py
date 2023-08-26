import math
import numpy as np
from stl import mesh

from src.config import GrooveConfig
from src.mesh_utils import square, build_mesh, join_meshes, apply_transform


class SegmentBuilder:
    def __init__(self, y0, l):
        self.z0 = 0
        self.y0 = y0
        self.faces = []
        self.l = l

    def add_point(self, delta_z, y):
        self.faces.append(_face(
            self.y0, y, self.z0, self.z0 + delta_z, self.l
        ))
        self.z0 = self.z0 + delta_z
        self.y0 = y


def create_groove_segment(
        l,
        d,
        h,
        ring_height,
        chamfer1_height,
        chamfer2_height,
        ring_delta_radius,
        groove_delta_radius,
        truncation_angle_1,
        truncation_angle_2,
):
    groove_height = h - 2 * chamfer1_height - 2 * chamfer2_height - 2 * ring_height
    builder = SegmentBuilder(d / 2, l)
    builder.add_point(chamfer1_height, d / 2 + ring_delta_radius)
    builder.add_point(ring_height, d / 2 + ring_delta_radius)
    builder.add_point(chamfer2_height, d / 2 + groove_delta_radius)
    builder.add_point(groove_height, d / 2 + groove_delta_radius)
    builder.add_point(chamfer2_height, d / 2 + ring_delta_radius)
    builder.add_point(ring_height, d / 2 + ring_delta_radius)
    builder.add_point(chamfer1_height, d / 2)

    faces = [
        _face(-d / 2, -d / 2, h, 0, l),
        *builder.faces,
    ]

    mesh = join_meshes(*faces)

    def bend_segment_transform(x, y, z):
        return x + y * math.tan(truncation_angle_1 if x > 0 else truncation_angle_2), y, z

    return apply_transform(mesh, bend_segment_transform)


def _face(y0, y1, z0, z1, l):
    vertices = np.array([
        [-l / 2, y0, z0],
        [-l / 2, y1, z1],
        [l / 2, y0, z0],
        [l / 2, y1, z1],
    ])
    faces = [
        *square(0, 1, 3, 2)
    ]
    return build_mesh(faces, vertices)


def generate_groove(config: GrooveConfig):
    truncation_angle = config.segment_center_angle / 2
    x_shape_width = 2 * config.radius * math.sin(truncation_angle)
    center_distance = config.radius * math.cos(truncation_angle)

    segments = []
    base_segment = create_groove_segment(
        x_shape_width,
        config.thickness,
        config.height,
        config.ring_height,
        config.chamfer1_height,
        config.chamfer2_height,
        config.ring_delta_radius,
        config.groove_delta_radius,
        truncation_angle,
        -truncation_angle,
    )

    for i in range(config.layer_segments_count):
        segment = mesh.Mesh(base_segment.data.copy())
        segment.translate(np.array([0, center_distance, 0]))
        segment.rotate(np.array([0, 0, 1]), config.segment_center_angle * i)
        segments.append(segment)

    return join_meshes(*segments)
