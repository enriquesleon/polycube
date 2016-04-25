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
    def __init__(self, piece_list, piece_id):
        self.cubes = list()
        self.piece_faces = list()
        self.rows = dict()
        self.unique_positions = set()
        self.original_cubes = piece_list
        self.piece_id = piece_id

        """The unique positions dictionary should contain unique rows with the key
            being a coordinate system to identify a piece+ position/orientation and the value
            being the cubes it occupies """

        self.cubes = self.num_list_to_coord_vector(piece_list)
        self.rotations = self.generate(self.cubes)
    def generate(self, piece):
        piece = self.fit_to_origin(piece)
        faces = self.get_piece_faces(piece)
        rotations = self.get_rotations(faces)
        return rotations

    def num_list_to_coord_vector(self, num_list):
        piece = list()
        for coord in num_list:
            x = coord % 5
            y = coord % 25 // 5
            z = coord // 25
            cube = [x, y, z]
            piece.append(cube)
            # self.cubes.append(cube)
        return piece

    def __add_piece_list_to_set(self, piece_list):
        for piece in piece_list:
            self.oringal_cubes_set.add(piece)

    def __rotate(self, piece, rotation_matrix, n):
        vectors = [np.matrix(cube).T for cube in piece]
        for i in range(n):
            vectors = [rotation_matrix.dot(vector) for vector in vectors]
        return [vector.T.tolist()[0] for vector in vectors]
        # self.cubes = [
            # rotation_matrix.dot(np.matrix(cube).T).T.tolist()[0] for cube in
            # self.cubes]

    def x_rotate(self, piece, n):
        return self.__rotate(piece, x_rot_matrix, n)

    def y_rotate(self, piece, n):
        return self.__rotate(piece, y_rot_matrix, n)

    def z_rotate(self, piece, n):
        return self.__rotate(piece, z_rot_matrix, n)

    def get_piece_faces(self, piece):
        piece = self.fit_to_origin(piece)
        face_0 = piece[:]
        face_1 = self.x_rotate(face_0, 1)
        face_2 = self.x_rotate(face_1, 1)
        face_3 = self.x_rotate(face_2, 1)
        face_4 = self.y_rotate(face_0, 1)
        face_5 = self.y_rotate(face_0, 3)
        return [face_0, face_1, face_2, face_3, face_4, face_5]

    def get_rotations(self, faces):
        rotations = list()
        for face in faces:
            fitted_face = self.fit_initial_config(face)
            rotations.append(fitted_face)
            for i in range(1, 4):
                rotation = self.z_rotate(face, i)
                rotation = self.fit_initial_config(rotation)
                rotations.append(rotation)
        return rotations

    def fit_to_origin(self, piece):
        """This should fit a piece until the origin cube lies at 0,0,0. Not all piece should
            have to be in bounds"""
        piece = self.sort_piece(piece)
        x_shift_d = -piece[0][0]
        y_shift_d = -piece[0][1]
        z_shift_d = -piece[0][2]
        piece = self.shift_x(piece, x_shift_d)
        piece = self.shift_y(piece, y_shift_d)
        piece = self.shift_z(piece, z_shift_d)
        return piece
        pass

    def shift_x(self, piece, n):
        for cube in piece:
            cube[0] = cube[0] + n
        return piece
        pass

    def shift_y(self, piece, n):
        for cube in piece:
            cube[1] = cube[1] + n
        return piece
        pass

    def shift_z(self, piece, n):
        for cube in piece:
            cube[2] = cube[2] + n
        return piece

    def fit_initial_config(self, piece):

        piece.sort(key=lambda k: k[0])
        x_shift_d = -piece[0][0]
        piece.sort(key=lambda k: k[1])
        y_shift_d = -piece[0][1]
        piece.sort(key=lambda k: k[2])
        z_shift_d = -piece[0][2]
        piece = self.shift_x(piece, x_shift_d)
        piece = self.shift_y(piece, y_shift_d)
        piece = self.shift_z(piece, z_shift_d)
        return self.sort_piece(piece)
        pass

    def fit_all_configs(self, rotations):

        unique_positions = set()
        unique_fit_rows = dict()
        initial_rotation_fits = [
            self.fit_initial_config(rotation) for rotation in rotations]
        """Essentially this should get the initial fit for all rotations.
            Then it should try to fit every piece into the cube.
            If it fit, try to add it the table. If some other rotation occupies the same space,
            Dont add it. We should also added some unique id string and append to a dictionary that 
            gets returned"""
        pass

    def vector_to_num_list(self, vector):
        """ Convert from an xyz coordinate into a number list for use in the algorithm"""
        x = vector[0]
        y = vector[1]
        z = vector[2]

        location = z * 25 + y * 5 + x
        return location

    def sort_piece(self, piece):
        piece = [self.vector_to_num_list(x) for x in piece]
        piece.sort()
        return self.num_list_to_coord_vector(piece)
        #piece.sort(key=lambda k: k[2])
        #piece.sort(key=lambda k: k[1])
        #piece.sort(key=lambda k: k[0])
        # return piece

    def __repr__(self):
        return str(self.cubes)

    def __str__(self):
        return str(self.cubes)

    def unique_string(self, cubes):
        s = ""
        num_list = [self.vector_to_num_list(cube) for cube in cubes]
        num_list.sort()
        for num in num_list:
            s = s + str(num) + ','
        return s


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
        new_piece = validate_piece_input_string(piece_input_line, piece_num)
    except ValueError as e:
        print(str(e))
        return None
    else:
        return new_piece


def validate_piece_input_string(piece_input, piece_num):
    piece_set = set()
    piece_split = piece_input.split(',')
    try:
        int(piece_split[0])
    except:
        raise ValueError('No Comma Serpated Values Found')

    piece_int_list = [int(x) for x in piece_split if int(x) >= 0]
    if len(piece_int_list) != len(piece_split):
        raise ValueError('No negative values allowed')
    for piece in piece_int_list:
        if piece in piece_set:
            raise ValueError('No duplicate values: ' + str(piece))
        else:
            piece_set.add(piece)
    new_piece = Piece(piece_int_list, piece_num)
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
        for rotation in piece.rotations:
            print(rotation)

if __name__ == '__main__':
    main()
