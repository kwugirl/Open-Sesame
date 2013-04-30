import serial
import math
import os

# this is the driver to get data off the device (Arduino + Wii nunchuck)
# run this to collect input from nunchuck

def main():
    ser = serial.Serial(port="/dev/tty.usbmodemfa131", baudrate=19200)
    # other port is "/dev/tty.usbmodemfd121"

    print ser.readline() # print out connection confirmation message

    while True: # keeping reading data from Arduino until c-button is pressed
        line = ser.readline() # reading serial output from Arduino line by line, program will hang here if no output
        data = str.strip(line) # strip newline from the end

        if data == "start": # z button pressed down for first time
            gesture = collect_data(ser)
            output_gesture(gesture)

        elif data == "exit":
            ser.close()
            return


def collect_data(ser):
    step = 30 # step for how frequently to record readings
    window = 50 # window to average across
    counter = step - window # start w/ neg number to be able to use mod later

    vectors = {} # dictionary for each list of averaging windows
    for i in range(3):
        vectors[i] = [0]*window

    gesture = []

    print "starting to collect data now"

    line = ser.readline()
    data = str.strip(line)

    while data != "stop": # stop = z button had been pressed down previously, now just let go of it to end collection of data
        print data

        values_list = str.split((data), ",") # break apart into a 3-item [x, y, z] list

        counter += 1

        for i in range(len(values_list)):
            values_list[i] = int(values_list[i]) # convert contents of vector_list into numbers
            vectors[i].pop(0) # pop off oldest value
            vectors[i].append(values_list[i]) # append newest value

        if counter % step == 0 and counter != 0: # for taking readings at the right steps (30, 60...) but skip when counter hits 0
            reading = get_avg_reading(vectors)
            gesture.append(reading)

        line = ser.readline()
        data = str.strip(line)

    return gesture

def output_gesture(gesture):
    print "finished collecting data"

    print gesture

    # writes out gesture data as text to wherever Mac OS can type right then
    output_cmd = """
    osascript -e 'tell application "System Events" to keystroke "%s"'
    """ %(str(gesture))

    os.system(output_cmd)
    # TO DO: terminal gets msg "dyld: DYLD_ environment variables being ignored because main executable (/usr/bin/osascript) is code signed with entitlements"

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


def convert_data(value):
    max_value = 256 # goes from 0-256 (1-255 for actual input)
    max_half = max_value/2
    levels_lower = 10 # for 0 to g
    levels_higher = 5 # for 0 to 2g

    value -= max_half # recenter for 128 to be at 0
    v = abs(value)

    if v > 0:
        sign = value/v # for whether it's positive or negative
    else:
        sign = 1 # for when input is 0 so that won't get division error

    # for 1 to 10 levels (including negative)
    if v <= max_half/2:
        step = max_value/(4.0*levels_lower)

        new_value = math.ceil(v/step)*sign

        return int(new_value)

    # for 11 to 15 levels (including negative)
    else:
        step = max_value/(4.0*levels_higher)
        v_diff = v - max_half/2 # difference from 64

        abs_value = math.ceil(v/step) + levels_lower # add 10 to get to 11-15
        new_value = abs_value*sign

        return int(new_value)


if __name__ == "__main__":
    main()