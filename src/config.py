import math


class BaseConfig:
    radius = 22
    height = 65
    thickness = 1.5
    base_cell_height = 22
    base_cell_width = 4
    contact_fraction_h = 0.3
    contact_fraction_v = 0.3
    frame_len_top = 0
    frame_len_bottom = 0
    x_shape_transform = None

    @property
    def height_without_frame(self):
        return self.height - self.frame_len_bottom - self.frame_len_bottom

    @property
    def layers_count(self):
        return round(self.height_without_frame / self.base_cell_height)

    @property
    def cell_height(self):
        return self.height_without_frame / self.layers_count

    def cell_fullness_function(self, angle, h_fraction):
        return 0


class CircularShapeConfig(BaseConfig):
    bottom = False
    open_top = False
    open_bottom = False

    @property
    def layer_cells_count(self):
        return round(math.pi * 2 * self.radius / self.base_cell_width)

    @property
    def cell_center_angle(self):
        return 2 * math.pi / self.layer_cells_count

    @property
    def truncation_angle(self):
        return self.cell_center_angle / 2

    @property
    def center_distance(self):
        return self.radius * math.cos(self.truncation_angle)


class GrooveConfig:
    ring_height = 2
    chamfer1_height = 2
    chamfer2_height = 2
    ring_delta_radius = 3
    groove_delta_radius = -3
    radius = 22
    height = 20
    thickness = 15
    base_cell_width = 4

    @property
    def layer_segments_count(self):
        return round(math.pi * 2 * self.radius / self.base_cell_width)

    @property
    def segment_center_angle(self):
        return 2 * math.pi / self.layer_segments_count

      
class SpiralShapeConfig(BaseConfig):
    roll_layers_gap = 3
    length = 100

    @property
    def a(self):  # "a" parameter of Archimedean spiral's equation
        return self.roll_layers_gap / math.pi

    def get_radius(self, angle):
        return self.a * angle + self.radius

    def get_point(self, angle):
        radius = self.get_radius(angle)
        return radius * math.cos(angle), radius * math.sin(angle)

    def get_center_angle(self, current_angle):  # good enough approximation
        return self.base_cell_width / self.get_radius(current_angle)
