import numpy as np
import copy
from collections import namedtuple

cube_size = 3
layer_size = cube_size *cube_size
x_rot_matrix = np.matrix([[1, 0, 0],
                          [0, 0, -1],
                          [0, 1, 0]])

y_rot_matrix = np.matrix([[0, 0, 1],
                          [0, 1, 0],
                          [-1, 0, 0]])

z_rot_matrix = np.matrix([[0, -1, 0],
                          [1, 0, 0],
                          [0, 0, 1]])

Rotation = namedtuple('Rotation', 'name piece')
Face = namedtuple('Face', 'name piece')
Fit = namedtuple('Fit','name piece')


class Piece:
    def __init__(self, piece_list, piece_id):
        self.cubes = list()
        self.original_cubes = piece_list
        self.piece_id = "P_" + str(piece_id)
        self.cubes = num_list_to_coord_vector(piece_list)
        self.generate()
        #self.rotations = self.generate(self.cubes, self.piece_id)

    def generate(self):
        self.fitted_piece = self.fit_to_origin(self.cubes)
        self.faces = self.get_piece_faces(self.fitted_piece, self.piece_id)
        self.rotations = self.get_rotations(self.faces)
        self.piece_dict = self.fit_all_configs(self.rotations)

    def num_list_to_coord_vector(self, num_list):
        piece = list()
        for coord in num_list:
            x = coord % cube_size
            y = coord % (layer_size) // cube_size
            z = coord // (layer_size)
            cube = [x, y, z]
            piece.append(cube)
        return piece

    def vector_to_num_list(self, piece):
        converted_piece = list()
        for cube in piece:
            x = cube[0]
            y = cube[1]
            z = cube[2]
            location = z * layer_size + y * cube_size + x
            converted_piece.append(location)
        return converted_piece

    def __add_piece_list_to_set(self, piece_list):
        for piece in piece_list:
            self.oringal_cubes_set.add(piece)

    def __rotate(self, piece, rotation_matrix, n):
        vectors = [np.matrix(cube).T for cube in piece]
        for i in range(n):
            vectors = [rotation_matrix.dot(vector) for vector in vectors]
        return [vector.T.tolist()[0] for vector in vectors]

    def x_rotate(self, piece, n):
        return self.__rotate(piece, x_rot_matrix, n)

    def y_rotate(self, piece, n):
        return self.__rotate(piece, y_rot_matrix, n)

    def z_rotate(self, piece, n):
        return self.__rotate(piece, z_rot_matrix, n)

    def get_piece_faces(self, piece, name=None):
        if name is None:
            name = "p_0"
        face_0 = Face(name + 'face_0', piece[:])
        face_1 = Face(name + 'face_1', self.x_rotate(face_0.piece, 1))
        face_2 = Face(name + 'face_2', self.x_rotate(face_1.piece, 1))
        face_3 = Face(name + 'face_3', self.x_rotate(face_2.piece, 1))
        face_4 = Face(name + 'face_4', self.y_rotate(face_0.piece, 1))
        face_5 = Face(name + 'face_5', self.y_rotate(face_0.piece, 3))
        return [face_0, face_1, face_2, face_3, face_4, face_5]

    def get_rotations(self, faces):
        rotations = list()
        unique_fits = set()
        for face in faces:
            fitted_face = self.fit_initial_config(face.piece)
            fitted_id = self.unique_string(fitted_face)
            if fitted_id not in unique_fits:
                unique_fits.add(fitted_id)
                rotations.append(Rotation(face.name + 'rot_0', fitted_face))
            for i in range(1, 4):
                rotation = self.z_rotate(face.piece, i)
                rotation = self.fit_initial_config(rotation)
                string_id = self.unique_string(rotation)
                if string_id not in unique_fits:
                    unique_fits.add(string_id)
                    rotations.append(
                        Rotation(face.name + 'rot_' + str(i), rotation))
        return rotations

    def fit_to_origin(self, piece):
        piece = self.sort_piece(piece)
        x_shift_d = -piece[0][0]
        y_shift_d = -piece[0][1]
        z_shift_d = -piece[0][2]
        piece = self.shift_x(piece, x_shift_d)
        piece = self.shift_y(piece, y_shift_d)
        piece = self.shift_z(piece, z_shift_d)
        return piece

    def shift_x(self, piece, n):
        shifted = [[cube[0]+n,cube[1],cube[2]] for cube in piece]
        #for cube in piece:
        #    cube[0] = cube[0] + n
        return shifted

    def shift_y(self, piece, n):
        shifted = [[cube[0],cube[1]+n,cube[2]] for cube in piece]
        
        #for cube in piece:
        #    cube[1] = cube[1] + n
        return shifted

    def shift_z(self, piece, n):
        shifted = [[cube[0],cube[1],cube[2]+n] for cube in piece]
        
        #for cube in piece:
        #    cube[2] = cube[2] + n
        return shifted

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

    def fit_all_configs(self, rotations):

        fits = list()
        for rotation in rotations:
            x_fits = self.get_x_fits(rotation)
            for xf in x_fits:
                y_fits = self.get_y_fits(xf)
                for yf in y_fits:
                    z_fits = self.get_z_fits(yf)
                    fits.extend(z_fits)
        return fits


    def get_x_fits(self,rotation):
        x_fits = list()
        max_x_shift=cube_size-sorted(rotation.piece,key=lambda k: k[0], reverse=True)[0][0]
        #print(max_x_shift)
        for x in range(max_x_shift):
            #print(self.shift_x(rotation.piece,x))
            x_fits.append(Fit(rotation.name + "X{}".format(x),self.shift_x(rotation.piece,x)))
        return x_fits
    def get_y_fits(self,rotation):
        y_fits =list()
        max_y_shift=cube_size-sorted(rotation.piece,key=lambda k: k[1], reverse=True)[0][1]

        for y in range(max_y_shift):
            y_fits.append(Fit(rotation.name + "Y{}".format(y),self.shift_y(rotation.piece,y)))
        return y_fits
    def get_z_fits(self,rotation):
        z_fits =list()
        max_z_shift=cube_size-sorted(rotation.piece,key=lambda k: k[2], reverse=True)[0][2]

        for z in range(max_z_shift):
            z_fits.append(Fit(rotation.name + "Z{}".format(z),vector_to_num_list(self.shift_z(rotation.piece,z))))
        return z_fits 



    def sort_piece(self, piece):
        piece = vector_to_num_list(piece)
        piece.sort()
        return num_list_to_coord_vector(piece)

    def __repr__(self):
        return str(self.cubes)

    def __str__(self):
        return str(self.cubes)

    def unique_string(self, cubes):
        s = ""
        num_list = vector_to_num_list(cubes)
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

def vector_to_num_list(piece):
        converted_piece = list()
        for cube in piece:
            x = cube[0]
            y = cube[1]
            z = cube[2]
            location = z * layer_size + y * cube_size + x
            converted_piece.append(location)
        return converted_piece
def num_list_to_coord_vector(num_list):
        piece = list()
        for coord in num_list:
            x = coord % cube_size
            y = coord % (layer_size) // cube_size
            z = coord // (layer_size)
            cube = [x, y, z]
            piece.append(cube)
        return piece

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
        for fit in piece.piece_dict:
            print (fit.name +":"+ str(fit.piece))
        #for rotation in piece.rotations:
            #print(str(rotation.piece) + rotation.name)
        #    pass

          #for k, v in piece.piece_dict.items():
            #print(k + str(v))


if __name__ == '__main__':
    main()
