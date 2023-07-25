import math
import vtkplotlib as vpl

from mpl_toolkits import mplot3d
from matplotlib import pyplot

from x_shape import _x_shape_quarter


# # Create a new plot
# figure = pyplot.figure()
# axes = mplot3d.Axes3D(figure)
#
# # Load the STL files and add the vectors to the plot
your_mesh = _x_shape_quarter(math.pi / 12, 0.2, 0.2)
# # your_mesh = mesh.Mesh.from_file('tests/stl_binary/HalfDonut.stl')
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#
# # Auto scale to the mesh size
# scale = your_mesh.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)
#
# # Show the plot to the screen
# pyplot.show()

plot = vpl.mesh_plot(your_mesh)
#
show = vpl.show(block=True)
# import ipdb; ipdb.set_trace()