from collections import namedtuple
import numpy

class Piece:
	cubes  = set()
	def get_cube_from_coord(self,line):
		line_parts = line.split(',')
		if len(line_parts) is not 3:
			raise ValueError('Line not in proper format')
		cube = [int(x) for x in line_parts]
		return cube
