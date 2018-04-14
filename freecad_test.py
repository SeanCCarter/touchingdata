"""
Step One: install Freecad
$ sudo add-apt-repository -y ppa:freecad-maintainers/freecad-stable
$ sudo apt-get update
$ sudo apt-get install freecad

Step Two: find the FreeCAD_PATH, likely in /opt or /usr/lib 
- look for the directory which contains FreeCAD.so
"""


FreeCAD_PATH = '/usr/lib/freecad/lib' # or wherever yours is installed to

import sys
sys.path.append('/usr/lib/freecad/lib')

import FreeCAD, Part, Units

# tu = Units.parseQuantity

# doc = FreeCAD.newDocument()

# box = doc.addObject("Part::Box", "myBox")

# doc.recompute()

# b = Part.makeBox(10,10,10)
# b.exportStl("box.stl")


import Mesh, BuildRegularGeoms
sphere = Mesh.Mesh( BuildRegularGeoms.Sphere(5.0, 50) )
cylinder = Mesh.Mesh( BuildRegularGeoms.Cylinder(2.0, 10.0, True, 1.0, 50) )
diff = sphere
diff = diff.difference(cylinder)
d = FreeCAD.newDocument("Sphereender")
d.addObject("Mesh::Feature","Diff_Sphere_Cylinder").Mesh=sphere
d.recompute()

objects = []
objects.append(FreeCAD.getDocument("Sphereender").getObject("Diff_Sphere_Cylinder"))
Mesh.export(objects, "/home/sean/Documents/Olin/Senior2/touchingdata/spherender.stl")

print "ok"