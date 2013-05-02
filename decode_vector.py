import base64
import struct


def decode(b64string):
    decoded_gesture = base64.b64decode(b64string)

    gesture_bytes = []
    for i in range(0, len(decoded_gesture), 4):
        # produces tuple of the two 1-byte numbers that make up 1 vector
        byte_pair = struct.unpack("hh", decoded_gesture[i:i+4])

        left_byte = byte_pair[0] << 8
        right_byte = byte_pair[1]

        vector = left_byte | right_byte

        gesture_bytes.append(vector)
    # print "consolidated xyz", gesture_bytes

    gesture_vectors = []
    for vector_packed in gesture_bytes:
        gesture_vectors.append(byte_unpack(vector_packed))
    print "unpacked vectors", gesture_vectors

    return gesture_vectors


def byte_unpack(vector):
    vector_list = []

    x = vector & int('000000000011111', 2)
    y = (vector & int('000001111100000', 2)) >> 5
    z = (vector & int('111110000000000', 2)) >> 10

    vector_list.append(x)
    vector_list.append(y)
    vector_list.append(z)

    for i in range(len(vector_list)):
        if vector_list[i] > 15:  # check if should be a negative value
            vector_list[i] = -1 * (vector_list[i] & 15)

    return vector_list
