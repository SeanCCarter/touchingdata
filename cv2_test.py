import cv2
import numpy as np

if __name__ == "__main__":
	gray_image = cv2.imread('graph3.png', cv2.IMREAD_GRAYSCALE)
	print len(gray_image)
	print len(gray_image[0])
	for row in range(len(gray_image)):
		for col in range(len(gray_image[row])):
			# pass
			gray_image[row][col] = 255 - gray_image[row][col]
	cv2.imwrite('gray_graph3.png', gray_image)
	print "yay"