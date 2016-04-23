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

    def num_list_to_coord_vector(self, num_list):
        for coord in num_list:
            x = coord % 5
            y = coord % 25 // 5
            z = coord // 25
            cube = np.matrix([[x], [y], [z]])
            self.cubes.append(cube)

    def __add_piece_list_to_set(self, piece_list):
        for piece in piece_list:
            self.oringal_cubes_set.add(piece)

    def x_rotate(self):
        self.cubes = [x_rot_matrix.dot(cube) for cube in self.cubes]

    def y_rotate(self):
        self.cubes = [y_rot_matrix.dot(cube) for cube in self.cubes]

    def z_rotate(self):
        self.cubes = [z_rot_matrix.dot(cube) for cube in self.cubes]

    def fit_initial_config(self):
        """From an XYZ vector, shift the position until all pieces lie in bounds"""
        pass

    def get_piece_config_rows(self):
        """Returns the unique configuration table and position for the piece"""
        pass

    def fit_all_configs(self):
        """Shift piece throughout cube space until all possible fittings are found"""
        pass

    def vector_to_num_list(self):
        """ Convert from an xyz coordinate into a number list for use in the algorithm"""
        pass


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
    for piece_order_num in piece_num:
        new_piece = enter_piece_input(piece_num)
        while new_piece is None:
            new_piece = enter_piece_input(piece_num)
        piece_list.append(new_piece)
    print(piece_list)

if __name__ == '__main__':
    main()
