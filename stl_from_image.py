"""
Making data (charts, graphs, &c.) accessible for people with visual impairments.
PerkinsHacks 2018 project by Matt Ruehle and Sean Carter

Dependencies: FreeCAD, OpenCV
"""


FreeCAD_PATH = '/usr/lib/freecad/lib' # or wherever yours is installed to

import sys
sys.path.append('/usr/lib/freecad/lib')

import FreeCAD, Part, Units

import cv2

import time

PIXEL_SIZE = 0.5
CANVAS_HEIGHT = 3*PIXEL_SIZE

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

class ModArray(object):

	def __init__(self, h, w, image):
		self.data = []
		for row in range(h):
			this_row = []
			for col in range(w):
				this_val = image[row][col]
				this_row.append(remap(this_val, 0, 255, 0, 7))
			self.data.append(this_row)

	def __getitem__(self, index):
		return self.data[index]

	def __setitem__(self, index, value):
		self.data[index] = value

	def get_nconsecutive_horizontal(self, row, col):
		this_val = self.data[row][col]
		n_cols = len(self.data[row])
		c = col
		n = 1
		while (c + n) < n_cols:
			if self.data[row][c+n] == this_val:
				n += 1
			else:
				break
		return n

	def get_nconsecutive_vertical(self, row, col):
		this_val = self.data[row][col]
		n_rows = len(self.data)
		r = row
		n = 1
		while (r + n) < n_rows:
			if self.data[r+n][col] == this_val:
				n += 1
			else:
				break
		return n

	def clear_horizontal(self, row, col, n):
		for i in range(n):
			self.data[row][col + i] = 0

	def clear_vertical(self, row, col, n):
		for i in range(n):
			self.data[row+i][col] = 0

	#improvement: getting wider rectangles, e.g. 4x4 instead of 4 1x4 ones, would improve efficiency.


def remap(val, old_low, old_high, new_low, new_high, to_int=True):
	proportion = float(val - old_low) / old_high
	target_range = new_high - new_low
	new_val = new_low + (proportion * target_range)
	if to_int:
		return int(new_val)
	return new_val

def create_pixel(row, col, val, row_length = 1, col_length=1):
	'''
	creates a pixel 
	of height (remap(val, 0, 255, 0, 6))
	at row, col pixels, of length row_length and width col_length.
	returns pixel, didCreate
	'''
	if val == 0:
		return None, False
	b = Part.makeBox(PIXEL_SIZE*row_length, PIXEL_SIZE*col_length, PIXEL_SIZE*val)
	v = FreeCAD.Vector(PIXEL_SIZE*row, PIXEL_SIZE*col, CANVAS_HEIGHT)
	b.translate(v)
	return b, True

def main(graph_name="example_image.png", stl_name=None):
	"""
	Creates a 3d model of the image; exports to an stl of stl_name
	"""
	t_start = time.time()
	doc = FreeCAD.newDocument()
	h, w, img = parse_image_gs_invert(graph_name)
	base = create_base(h, w)
	mod_array = ModArray(h, w, img)
	for row in range(h):
		sys.stdout.write("row %s of %s\r" % (str(row), str(h)))
		sys.stdout.flush()
		for col in range(w):
			n_horiz = mod_array.get_nconsecutive_horizontal(row, col)
			n_vert = mod_array.get_nconsecutive_vertical(row, col)
			if n_vert > n_horiz:
				new_pix, didCreate = create_pixel(row, col, mod_array[row][col], row_length=n_vert)
				mod_array.clear_vertical(row, col, n_vert)
			else:
				new_pix, didCreate = create_pixel(row, col, mod_array[row][col], col_length=n_horiz)
				mod_array.clear_horizontal(row, col, n_horiz)
			if didCreate:
				base = base.fuse(new_pix)
	print ''
	if stl_name == None:
		stl_name = graph_name + ".stl"
	base.exportStl(stl_name)
	print "time elapsed: ", (time.time() - t_start)


if __name__ == "__main__":
	main()