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

import cv2
import numpy as np

import time

PIXEL_SIZE = 0.1 # mm
CANVAS_HEIGHT = 1*PIXEL_SIZE

def parse_image_gs_invert(filename):
	""" 
	filename: 'file_name.png' or something
	grayscale's the image
	inverts the image (so, if there's black lines on a white background, that's ok).
	returns height, width, image
	"""
	gray_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	height = len(gray_image)
	width = len(gray_image[0])
	for row in range(height):
		for col in range(width):
			gray_image[row][col] = 255 - gray_image[row][col]
	return height, width, gray_image

def create_base(width, length):
	b = Part.makeBox(width*PIXEL_SIZE, length*PIXEL_SIZE, CANVAS_HEIGHT)
	return b

def remap(val, old_low, old_high, new_low, new_high, to_int=True):
	proportion = float(val - old_low) / old_high
	target_range = new_high - new_low
	new_val = new_low + (proportion * target_range)
	if to_int:
		return int(new_val)
	return new_val

def create_pixel(row, col, val):
	'''
	creates a pixel 
	of height (remap(val, 0, 255, 0, 6))
	returns pixel, didCreate
	'''
	pixel_height = remap(val, 0, 255, 0, 6)
	if pixel_height == 0:
		return None, False
	b = Part.makeBox(PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
	v = FreeCAD.Vector(PIXEL_SIZE*row, PIXEL_SIZE*col, CANVAS_HEIGHT)
	b.translate(v)
	return b, True


def main(graph_name="graph3.png"):
	t_start = time.time()
	doc = FreeCAD.newDocument()
	h, w, img = parse_image_gs_invert(graph_name)
	base = create_base(h, w)
	# shapelist = [base]
	# shapelist = []
	for row in range(h):
		sys.stdout.write("row %s of %s\r" % (str(row), str(h)))
		sys.stdout.flush()
		for col in range(w):
			# shapelist.append(create_pixel(row, col, img[row][col]))
			new_pix, didCreate = create_pixel(row, col, img[row][col])
			if didCreate:
				base = base.fuse(new_pix)
		# 	doc.removeObject(new_pix.Label)
	print ' '
	# merged = Part.makeCompound(shapelist)
	# merged.exportStl("graph_box.stl")
	base.exportStl("gbox.stl")
	
	print "time elapsed: ", (time.time() - t_start)

main()

# optimize: perhaps, instead of making each pixel by pixel, get as many consecutive identical ones as possible.
# doc = FreeCAD.newDocument()

# box = doc.addObject("Part::Box", "myBox")

# doc.recompute()


# b = Part.makeBox(10,10,10)
# b2 = create_base(600,600)
# b = b.fuse(b2)
# b.exportStl("box.stl")
# print "ok"