import dtw_algorithm
import math


def test_dtw():
    # Christian's example from 4/10 talk
    """
    desired end matrix looks like this: doing min of (cell above, to left, or diagonal to the upper left), going from top left to bottom right:
    0       (1)inf (2)inf   (1)inf
    (1)inf  0       1       1
    (1)inf  0       1       1
    (2)inf  1       0       1
    (1)inf  1       1       0*
    """
    a = [1, 2, 1]
    b = [1, 1, 2, 1]
    assert(dtw_algorithm.dtw(a, b) == 0), "Basic Euclidean-distance based test failed"

    s1 = sine_wave(360, 1)
    s2 = sine_wave(360, 2)
    assert(dtw_algorithm.dtw(s1, s2) < 2), "Sine wave test failed"


# given degrees and step size, product and return list of vectors for a sine wave
def sine_wave(degrees, step):
    vector_list = []
    for i in range(1, degrees, step):
        vector = math.sin(math.radians(i))
        vector_list.append(vector)

    return vector_list
