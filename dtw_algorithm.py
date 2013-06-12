import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):  # for if you were to subtract one vector object from another, uses Pythagorean theorem
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z

        distance = math.sqrt(x ** 2 + y ** 2 + z ** 2)

        return distance


class Gesture:
    def __init__(self, vectors):  # pass in list of Vector objects to create a Gesture
        self.vectors = vectors

    def __sub__(self, other):  # to subtract one gesture from another (to get the difference, lower difference = more similar)
        return dtw(self.vectors, other.vectors)


def create_gesture(vector_list):
    vector_objects = []

    for vector in vector_list:  # convert vector data into vector objects
        new_vector = Vector(vector[0], vector[1], vector[2])
        vector_objects.append(new_vector)

    return Gesture(vector_objects)


def distance_euclidean(a, b):
    return abs(a-b)


# instead of building whole matrix, just build one row at a time to be more memory efficient
def dtw(x_axis, y_axis, distance=distance_euclidean):
    # set up foundation row
    row = []
    current_x = x_axis[0]
    for val_y in y_axis:
        row.append(distance_euclidean(current_x, val_y))

    for position_x in range(1, len(x_axis)):
        current_x = x_axis[position_x]

        temp = row[0]
        row[0] = distance_euclidean(current_x, y_axis[0]) + row[0]

        for i in range(1, len(y_axis)):
            temp_2 = row[i]

            row[i] = distance_euclidean(current_x, y_axis[i]) + min(row[i-1], temp, temp_2)

            temp = temp_2

    return row[-1]


# algorithm from http://en.wikipedia.org/wiki/Dynamic_time_warping#Implementation
def dtw_old(x_axis, y_axis, distance=distance_euclidean):  # set_a and set_b are lists, default distance fn to use is distance_euclidean but could pass in a different fn to use instead if needed
    x = len(x_axis) + 1
    y = len(y_axis) + 1

    dtw_matrix = build_borders(x, y)

    # #for loops go from (1, 1) to (1, y-1) positions, then (2, 1) to (2, y-1) until you end up with a value for (x-1, y-1)
    for i in range(1, x):
        for j in range(1, y):
            # get distance value for the cell
            d = distance(x_axis[i-1], y_axis[j-1])

            # fill in cell with distance plus min of earlier cell (above, to left, or diagonal towards origin)
            dtw_matrix[i][j] = d + min(dtw_matrix[i-1][j],
                                        dtw_matrix[i][j-1],
                                        dtw_matrix[i-1][j-1])

    # print out what matrix looks like
    # for j in range(0, y):
    #   for i in range(0, x):
    #       print dtw_matrix[i][j],
    #   print ""

    return dtw_matrix[x-1][y-1]


def build_borders(x, y):
    # make empty matrix (list of lists) that are x across and y deep
    dtw_matrix = [0]*x  # set up matrix's full length along x-axis
    for j in range(x):
        temp_list = []
        for i in range(y):
            temp_list.append([])  # set up matrix's full length along y-axis
        dtw_matrix[j] = temp_list  # do it this way so that don't get a list of the same list over and over again, next line wouldn't work to only change value for one cell in matrix

    dtw_matrix[0][0] = 0  # set first box to be 0 as starting point

    # fill in top/left borders of matrix with infinity
    inf = float("inf")  # use this way to get infinity as a value in Python
    for i in range(1, x):
        dtw_matrix[i][0] = inf
    for i in range(1, y):
        dtw_matrix[0][i] = inf

    return dtw_matrix
