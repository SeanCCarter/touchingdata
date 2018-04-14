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

tu = Units.parseQuantity

doc = FreeCAD.newDocument()

box = doc.addObject("Part::Box", "myBox")

doc.recompute()

print "ok"