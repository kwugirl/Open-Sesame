import serial
import math
import os
import struct
import base64

# this is the driver to get data off the device (Arduino + Wii nunchuck)
# run this to collect input from nunchuck


def main():
    ser = serial.Serial(port="/dev/tty.usbmodemfa131", baudrate=19200)
    # other port is "/dev/tty.usbmodemfd121"

    print ser.readline()  # print out connection confirmation message

    while True:  # keeping reading data from Arduino until c-button is pressed
        line = ser.readline()  # reading serial output from Arduino line by line, program will hang here if no output
        data = str.strip(line)  # strip newline from the end

        if data == "start":  # z button pressed down for first time
            # gesture = collect_data_raw(ser)
            gesture = collect_data_windows(ser)
            output_gesture(gesture)

        elif data == "exit":
            ser.close()
            return


def collect_data_windows(ser):
    # changed step and window from 30 and 50 as in U-Wave paper due to nunchuck reading freq at ~100hz
    step = 3  # step for how frequently to record readings
    window = 5  # window to average across
    counter = step - window  # start w/ neg number to be able to use mod later

    vectors = {}  # dictionary for each list of averaging windows
    for i in range(3):
        vectors[i] = [0]*window

    gesture = []

    print "starting to collect data now"

    line = ser.readline()
    data = str.strip(line)

    while data != "stop":  # stop = z button had been pressed down previously, now just let go of it to end collection of data
        print data

        values_list = str.split((data), ",")  # break apart into a 3-item [x, y, z] list

        counter += 1

        # add each new xyz value to the right list in the vectors dictionary
        for i in range(len(values_list)):
            values_list[i] = int(values_list[i])  # convert contents of vector_list into numbers
            vectors[i].pop(0)  # pop off oldest value
            vectors[i].append(values_list[i])  # append newest value

        # take readings at the right steps (30, 60...) but skip when counter hits 0
        if counter % step == 0 and counter != 0:
            reading = get_avg_reading(vectors)
            # reading_packed = byte_pack(reading)
            gesture.append(reading)

        line = ser.readline()
        data = str.strip(line)

    return gesture


# def collect_data_raw(ser):
#     gesture = []

#     print "starting to collect data now"

#     line = ser.readline()
#     data = str.strip(line)

#     while data != "stop":
#         print data

#         values_list = str.split((data), ",")
#         for i in range(len(values_list)):
#             values_list[i] = int(values_list[i])
#             values_list[i] = convert_data(values_list[i])

#         gesture.append(values_list)

#         line = ser.readline()
#         data = str.strip(line)

#     return gesture


def output_gesture(gesture):
    print "finished collecting data"

    print "all vectors: ", gesture
    print "full gesture length: ", len(gesture)

    encoded_gesture = encode_gesture(gesture)

    # writes out gesture data as text to wherever Mac OS can type right then
    output_cmd = """
    osascript -e 'tell application "System Events" to keystroke "%s"'
    """ % (encoded_gesture)

    os.system(output_cmd)
    # TODO: terminal gets msg "dyld: DYLD_ environment variables being ignored because main executable (/usr/bin/osascript) is code signed with entitlements"


def get_avg_reading(vectors):
    reading = []

    for i in range(3):
        avg = get_avg(vectors[i])
        converted_value = convert_data(avg)

        reading.append(converted_value)

    return reading


def get_avg(numbers):
    sum = 0
    for num in numbers:
        sum += num
    avg = sum / len(numbers)

    return avg


# given vector value, scale it to be between -16 and +16
def convert_data(value):
    max_value = 256  # goes from 0-256 (1-255 for actual input)
    max_half = max_value/2
    levels_lower = 10  # for 0 to g
    levels_higher = 5  # for 0 to 2g

    value -= max_half  # recenter for 128 to be at 0
    v = abs(value)

    if v > 0:
        sign = value/v  # for whether it's positive or negative
    else:
        sign = 1  # for when input is 0 so that won't get division error

    # for 1 to 10 levels (including negative)
    if v <= max_half/2:
        step = max_value/(4.0*levels_lower)

        new_value = math.ceil(v/step)*sign

        return int(new_value)

    # for 11 to 15 levels (including negative)
    else:
        step = max_value/(4.0*levels_higher)
        v_diff = v - max_half/2  # difference from 64

        abs_value = math.ceil(v_diff/step) + levels_lower  # add 10 to get to 11-15
        new_value = abs_value*sign

        return int(new_value)


# given set of xyz vectors, get back one 15-bit number to represent all 3
def byte_pack(vector_list):
    for i in range(len(vector_list)):
        if vector_list[i] < 0:  # to handle negative numbers, use 5th bit as signed bit
            vector_list[i] = abs(vector_list[i]) | 16  # "bitwise or" with 16

        vector_list[i] = vector_list[i] & 31  # "bitwise and" to get 5 bits of data
        vector_list[i] = vector_list[i] << i*5  # left shift 2nd and 3rd numbers

    vector_packed = 0
    for vector in vector_list:
        vector_packed = vector_packed | vector  # "bitwise or" all three numbers together

    return vector_packed


# given list of byte-packed vectors (each 2-byte number is one vector), get base64 encoded version back
def encode_gesture(gesture):
    gesture_consolidated = []
    for vector in gesture:
        gesture_consolidated.append(byte_pack(vector))
    print "xyz consolidated: ", gesture_consolidated

    gesture_bytes = []
    for vector in gesture_consolidated:
    # break each 15-bit vector number into two halves (2 bytes)
        left_byte = (vector & 0xFF00) >> 8  # get left half, shift by 8 to make 8-bit number

        right_byte = vector & 0x00FF  # get right right

        byte_pair = struct.pack("hh", left_byte, right_byte)
        gesture_bytes.append(byte_pair)
    print "byte pairs: ", gesture_bytes

    encoded_gesture = base64.b64encode(''.join(gesture_bytes))

    return encoded_gesture


if __name__ == "__main__":
    main()
