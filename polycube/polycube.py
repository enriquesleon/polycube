import numpy as np
from math import cos
from math import sin


x_rot = [[1, 0, 0],
         [0, 0, -1],
         [0, 1, 0]]

y_rot = [[0, 0, 1],
         [0, 1, 0],
         [-1, 0, 0]]

z_rot = [[0, -1, 0],
        [1, 0, 0], 
        [0, 0, 1]]


class Piece:
    def __init__(self, piece_string):
        self.cubes = list()
        self.piece_string = piece_string
        self.num_list = self.piece_string_to_num(piece_string)
        self.num_list_to_coord(self.num_list)

    def num_list_to_coord(self, num_list):
        for coord in num_list:
            x = coord % 5
            y = coord % 25 // 5
            z = coord // 25
            cube = [[x], [y], [z]]
            self.cubes.append(cube)

    def piece_string_to_num(self, line):
        parts = line.split(',')
        num_list = []
        return [int(x) for x in parts]
