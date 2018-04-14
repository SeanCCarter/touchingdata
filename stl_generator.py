FreeCAD_PATH = '/usr/lib/freecad/lib' # or wherever yours is installed to

import sys
sys.path.append('/usr/lib/freecad/lib')

import FreeCAD, Part, Units
from FreeCAD import Base
from PIL import Image
import numpy as np
import math
im = Image.open("zebra.png")
pix = im.load()


def scatterPlot(my_data, dot_size = 5, height = 10, scale = (100, 100), axis = (10,10)):
	#Create Axis
	gsize = (1000, 1000)
	mybaseshape = Part.makeBox(gsize[0]+30,gsize[1]+30,1)
	xaxis = Part.makeBox(gsize[0],10, height + 1)
	xaxis.translate(Base.Vector(0,30,1))
	yaxis = Part.makeBox(10,gsize[1],height + 1)
	yaxis.translate(Base.Vector(30,0,1))
	mybaseshape = mybaseshape.fuse(xaxis)
	mybaseshape = mybaseshape.fuse(yaxis)

	#add x gridlilnes
	for i in range(axis[0]):
		gridline = Part.makeBox(5,gsize[0],height/4 + 1)
		gridline.translate(Base.Vector(30 + i*gsize[0]/axis[0],0,1))
		mybaseshape = mybaseshape.fuse(gridline)

	#add y gridlilnes
	for i in range(axis[1]):
		gridline = Part.makeBox(gsize[1],5,height/4 + 1)
		gridline.translate(Base.Vector(0,30 + i*gsize[1]/axis[1],1))
		mybaseshape = mybaseshape.fuse(gridline)

	for point in my_data:
		x = int(point[0]*float(gsize[0])/scale[0])
		y = int(point[1]*float(gsize[1])/scale[1])
		cylander = Part.makeCylinder(dot_size,height,Base.Vector(x+35,y+35,0))
		#cylander.translate(Base.Vector(x+35,y+35,0))
		mybaseshape = mybaseshape.fuse(cylander)

	return mybaseshape

def lineGraph(my_data, line_width = 5, height = 10, scale = (100, 100), axis = (10,10)):
	#Create Axis
	gsize = (1000, 1000)
	mybaseshape = Part.makeBox(gsize[0]+30,gsize[1]+30,1)
	xaxis = Part.makeBox(gsize[0],10, height + 1)
	xaxis.translate(Base.Vector(0,30,1))
	yaxis = Part.makeBox(10,gsize[1],height + 1)
	yaxis.translate(Base.Vector(30,0,1))
	mybaseshape = mybaseshape.fuse(xaxis)
	mybaseshape = mybaseshape.fuse(yaxis)

	#add x gridlilnes
	for i in range(axis[0]):
		gridline = Part.makeBox(5,gsize[0],height/4 + 1)
		gridline.translate(Base.Vector(30 + i*gsize[0]/axis[0],0,1))
		mybaseshape = mybaseshape.fuse(gridline)

	#add y gridlilnes
	for i in range(axis[1]):
		gridline = Part.makeBox(gsize[1],5,height/4 + 1)
		gridline.translate(Base.Vector(0,30 + i*gsize[1]/axis[1],1))
		mybaseshape = mybaseshape.fuse(gridline)

	for i, point in enumerate(my_data[:-1]):
		nextpoint = my_data[i+1]
		partCylinder = Part.makeCylinder(5,20,Base.Vector(20,0,0),Base.Vector(0,0,1),180)
		x1 = int(point[0]*float(gsize[0])/scale[0]) + 35
		y1 = int(point[1]*float(gsize[1])/scale[1]) + 35
		x2 = int(nextpoint[0]*float(gsize[0])/scale[0]) + 35
		y2 = int(nextpoint[1]*float(gsize[1])/scale[1]) + 35

		dist = math.hypot(x2 - x1, y2 - y1)
		#box = Part.makeBox(line_width,height,dist,Base.Vector(x1,y1,height),Base.Vector(x2-x1,y2-y1,0))
		partCylinder = Part.makeCylinder(line_width,dist,Base.Vector(x1,y1,0),Base.Vector(x2-x1,y2-y1,0),360)
		mybaseshape = mybaseshape.fuse(partCylinder)

	return mybaseshape

x = np.arange(0.0, 50.0, 2.0)
y = x ** 1.3 + np.random.rand(*x.shape) * 30.0

points = zip(x,y)

stl = scatterPlot(points, height=15, dot_size = 10, scale=(50,180))
stl.exportStl("/home/sean/Documents/Olin/Senior2/touchingdata/scatter.stl")

stl2 = lineGraph(points, height=15, line_width = 10, scale=(50,180))
stl2.exportStl("/home/sean/Documents/Olin/Senior2/touchingdata/linegraph.stl")
