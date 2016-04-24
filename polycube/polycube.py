import numpy as np


x_rot_matrix = np.matrix([[1, 0, 0],
                          [0, 0, -1],
                          [0, 1, 0]])

y_rot_matrix = np.matrix([[0, 0, 1],
                          [0, 1, 0],
                          [-1, 0, 0]])

z_rot_matrix = np.matrix([[0, -1, 0],
                          [1, 0, 0],
                          [0, 0, 1]])


class Piece:
    def __init__(self, piece_list):
        self.cubes = list()
        self.oringal_cubes_set = set()
        self.piece_list = piece_list
        self.__add_piece_list_to_set(piece_list)
        if len(self.oringal_cubes_set) != len(piece_list):
            raise ValueError("There is some duplicate value entered")
        self.num_list_to_coord_vector(piece_list)
        print(piece_list)

    def num_list_to_coord_vector(self, num_list):
        for coord in num_list:
            x = coord % 5
            y = coord % 25 // 5
            z = coord // 25
            cube = [[x],[y],[z]]
            #cube = np.matrix([[x], [y], [z]])
            self.cubes.append(cube)
            print(cube)

    def __add_piece_list_to_set(self, piece_list):
        for piece in piece_list:
            self.oringal_cubes_set.add(piece)

    def __rotate(self, rotation_matrix):
        for cube in self.cubes:
            cube = rotation_matrix.dot(cube)

    def x_rotate(self):
        self.__rotate(x_rot_matrix)

    def y_rotate(self):
        self.__rotate(y_rot_matrix)

    def z_rotate(self):
        self.__rotate(z_rot_matrix)

    def fit_initial_config(self):
        """From an XYZ vector, shift the position until all pieces lie in bounds"""
        pass

    def get_piece_config_rows(self):
        """Returns the unique configuration table and position for the piece"""
        pass

    def fit_all_configs(self):
        """Shift piece throughout cube space until all possible fittings are found"""
        pass

    def vector_to_num_list(self, vector):
        """ Convert from an xyz coordinate into a number list for use in the algorithm"""
        x = vector.item(0)
        y = vector.item(1)
        z = vector.item(2)

        location = z * 25 + y * 5 + x
        return location
    def __repr__(self):
        return str(self.cubes)
    def __str__(self):
        return str(self.cubes)



def validate_pos_num_string(line_input):
    try:
        num = int(line_input)
    except:
        return None
    if num <= 0:
        return None
    else:
        return num


def enter_piece_input(piece_num):
    piece_input_line = input(
        'Enter piece input. Must be unique comma seperated Values:')
    try:
        new_piece = validate_piece_input_string(piece_input_line)
    except ValueError as e:
        print(str(e))
        return None
    else:
        return new_piece


def validate_piece_input_string(piece_input):
    piece_split = piece_input.split(',')
    if len(piece_split) == 1:
        raise ValueError('Comma Serpated Values Found')
    piece_int_list = [int(x) for x in piece_split if int(x) >= 0]
    if len(piece_int_list) != len(piece_split):
        raise ValueError('No negative values allowed')
    try:
        new_piece = Piece(piece_int_list)
    except ValueError as e:
        raise e
    else:
        return new_piece


def main():
    piece_list = list()
    piece_num_input = input("How many pieces?")
    piece_num = validate_pos_num_string(piece_num_input)
    if piece_num is None:
        raise ValueError('Incorrect Input type. Must be a positive int')
    for piece_order_num in range(piece_num):
        new_piece = enter_piece_input(piece_num)
        while new_piece is None:
            new_piece = enter_piece_input(piece_num)
        piece_list.append(new_piece)
    for piece in piece_list:
        print(piece)

if __name__ == '__main__':
    main()
