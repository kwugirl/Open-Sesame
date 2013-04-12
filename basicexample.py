# make matrix of products given two lists of values for x/y-axis
def distance_matrix(x_axis, y_axis):
	x_size = len(x_axis)
	y_size = len(y_axis)

	matrix = [0]*y_size # set up matrix's full length along y-axis

	for j in range(y_size):
		temp_list = []
		for i in range(x_size):
			value = distance(x_axis[i], y_axis[j]) # this is the value to put into the matrix at position (i, j)
			temp_list.append(value)
		matrix[j] = temp_list

	return matrix

# calculate distance between two given points
def distance(a, b):
	return abs(a-b)

def warped_matrix(matrix):
	new_matrix = matrix

	for y in range(len(matrix[0])):
		for x in range(len(matrix)):
			new_matrix[x][y] = cell_value(matrix, x, y)

	return new_matrix

# what to fill in cell, given the position (x, y) of the cell in that matrix
# only doing min of cell above or to left, going from top left to bottom right
def cell_value(matrix, x, y):
	if x == 0 or y == 0: # to handle items along edges so it doesn't go into negative indexes for the lists in the matrix
		if x == 0 and y == 0: # starting position
			prev = 0
		elif x == 0 and y > 0: # along top edge (x = 0)
			prev = matrix[0][y-1]
		else: # should be y == 0 and x > 0 True, along left edge (y = 0)
			prev = matrix[x-1][y]
	else:
		prev = min(matrix[x-1][y], matrix[x][y-1])

	v = matrix[x][y] + prev

	return v

"""
build matrix of set A on one axis vs. set B on another axis
create matrix of local distance (abs. value)
create 2nd matrix of local distance (abs. value) + min of distance in previous cells that are closer to the origin cell
determine lowest value path (sum values to get path value, and do so for all potential paths?)
get coordinates of lowest value path
calculate difference between lowest value path and perfect diagonal for "similarity score"
"""

# Christian's example from 4/10 talk
a = 1, 2, 1
b = 1, 1, 2, 1
"""
first distance matrix should look like this:
	1 	2 	1
1]	0	1 	0
1]	0	1 	0
2]	1 	0 	1
1] 	0 	1 	0

temp_list=[]
temp_list.append(a[0]*b[0])
temp_list.append(a[1]*b[0])
temp_list.append(a[2]*b[0])
matrix[0] = temp_list

temp_list=[]
temp_list.append(a[0]*b[1])
temp_list.append(a[1]*b[1])
temp_list.append(a[2]*b[1])
matrix[1] = temp_list

second warped matrix should look like this, only doing min of cell above or to left, going from top left to bottom right:
	1 	2 	1
1]	0	1 	1
1]	0	1 	1
2]	1 	1 	2
1] 	1 	2 	2*
"""