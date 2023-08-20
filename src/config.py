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

    @property
    def height_without_frame(self):
        return self.height - self.frame_len_bottom - self.frame_len_bottom

    @property
    def layers_count(self):
        return round(self.height_without_frame / self.base_cell_height)

    @property
    def cell_height(self):
        return self.height_without_frame / self.layers_count


class CircularShapeConfig(BaseConfig):
    bottom = False

    def cell_fullness_function(self, angle, h_fraction):
        return 0

    @property
    def layer_cells_count(self):
        return round(math.pi * 2 * self.radius / self.base_cell_width)

    @property
    def cell_center_angle(self):
        return 2 * math.pi / self.layer_cells_count



'''
pattern: spherical
radius: 22
height: 65
thickness: 1.5
x_height: 22
x_width: 4
contact_fraction_h: 0.3
contact_fraction_v: 0.3
frame_len_top: 0
frame_len_bottom: 2
fullness_function: linear
warp_function: bowl
bottom: true
'''
