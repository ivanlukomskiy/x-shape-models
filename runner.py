import math

from x_shape import _x_shape_quarter

mesh = _x_shape_quarter(math.pi / 12, 0.2, 0.2,
                        # top_cap=True,
                        # bottom_cap=True,
                        # top_patch=True,
                        # bottom_patch=True,
                        # right_patch=True,
                        # right_cap=True,
                        # left_patch=True,
                        # left_cap=True,
                        )

mesh.save('viewer/wider.stl')
