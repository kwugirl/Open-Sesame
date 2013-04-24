from pyprocessing import *

# playing around with pyprocessing library

def setup():
    size(800, 800)


def draw():

    vector_list = [[6, -7, 4], [7, -6, 6], [-3, -6, 8], [-4, -5, 5], [-5, 3, 8], [-10, 6, 10], [-6, 2, 6], [-6, 2, 10]]

    vector_list_2 = [[-9, 4, 7], [-9, 5, 7], [-7, -2, 6], [-3, -6, 7], [2, -6, 9]]

    sum_x = 0
    sum_y = 0
    sum_z = 0

    background(255)

    translate(100, 100, 0) # translate resets where origin is

    for vector in vector_list:
        point(0,0,0)

        v = PVector(vector[0], vector[1], vector[2])

        line(0,0,0, v.x, v.y, v.z)

        translate(v.x, v.y, v.z)

        sum_x += v.x
        sum_y += v.y
        sum_z += v.z

    translate(-sum_x+100, -sum_y, -sum_z) # translate resets where origin is

    point(0,0,0)

    for vector in vector_list_2:
        point(0,0,0)

        v = PVector(vector[0], vector[1], vector[2])

        line(0,0,0, v.x, v.y, v.z)

        translate(v.x, v.y, v.z)

def plot():
    run()

