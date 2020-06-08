from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import Box
from compas.geometry import Sphere
from compas.datastructures import Mesh
from compas.datastructures import mesh_subdivide_quad

from compas_rhino.artists import MeshArtist

from compas.rpc import Proxy

booleans = Proxy('compas_cgal.booleans')

# ==============================================================================
# Make a box and a sphere
# ==============================================================================

R = 1.4

O = Point(0, 0, 0)
X = Vector(1, 0, 0)
Y = Vector(0, 1, 0)
Z = Vector(0, 0, 1)
YZ = Plane(O, X)
ZX = Plane(O, Y)
XY = Plane(O, Z)

box = Box.from_width_height_depth(2 * R, 2 * R, 2 * R)
box = Mesh.from_shape(box)
box = mesh_subdivide_quad(box, k=1)
box.quads_to_triangles()

sphere = Sphere(O, 1.25 * R)
sphere = Mesh.from_shape(sphere, u=50, v=50)
sphere.quads_to_triangles()

# ==============================================================================
# Compute the boolean mesh
# ==============================================================================

# Note that the automatic remeshing works well on the difference of cube and sphere
# because the difference has very sharp edges at the intersection between the tow shapes.
# A more general approach to remeshing would protect the edges found at the intersection,
# regardless of whether they are sharp or not.

V, F = booleans.boolean_difference(
    box.to_vertices_and_faces(),
    sphere.to_vertices_and_faces())

mesh = Mesh.from_vertices_and_faces(V, F)

# ==============================================================================
# Visualize
# ==============================================================================

artist = MeshArtist(mesh, layer="CGAL::Booleans::Difference")
artist.clear_layer()

artist.draw_faces(join_faces=True)

artist.redraw()