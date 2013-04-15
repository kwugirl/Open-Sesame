import math

# algorithm from http://en.wikipedia.org/wiki/Dynamic_time_warping#Implementation
def dtw(x_axis, y_axis): # set_a and set_b are lists
    x = len(x_axis) + 1
    y = len(y_axis) + 1

    # make empty matrix (list of lists) that are x across and y deep
    dtw_matrix = [0]*x # set up matrix's full length along x-axis
    for j in range(x):
        temp_list = []
        for i in range(y):
            temp_list.append([]) # set up matrix's full length along y-axis
        dtw_matrix[j] = temp_list # do it this way so that don't get a list of the same list over and over again, next line wouldn't work to only change value for one cell in matrix

    dtw_matrix[0][0] = 0 # set first box to be 0 as starting point

    # fill in top/left borders of matrix with infinity
    inf = float("inf") # use this way to get infinity as a value in Python
    for i in range(1,x):
        dtw_matrix[i][0] = inf
    for i in range(1,y):
        dtw_matrix[0][i] = inf

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

def distance(a, b):
    return abs(a-b)

# Christian's example from 4/10 talk
a = 1, 2, 1
b = 1, 1, 2, 1
"""
desired end matrix looks like this: doing min of (cell above, to left, or diagonal to the upper left), going from top left to bottom right:
0       (1)inf (2)inf   (1)inf
(1)inf  0       1       1
(1)inf  0       1       1
(2)inf  1       0       1
(1)inf  1       1       0*
"""

# given degrees and step size, product and return list of vectors for a sine wave
def sine_wave(degrees, step):
    vector_list = []
    for i in range(1, degrees, step):
        vector = math.sin(math.radians(i))
        vector_list.append(vector)

    return vector_list

l1 = sine_wave(360, 1)
l2 = sine_wave(360, 2)
#dtw(l1, l2) should be < 2