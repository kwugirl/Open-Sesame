import serial
import math
# this is the driver to get data off the device (Arduino + Wii nunchuck)

def read():
    ser = serial.Serial(port="/dev/tty.usbmodemfa131", baudrate=19200, timeout= 3) # will time out any .readline() below after 3 seconds
    # other port is "/dev/tty.usbmodemfd121"

    print ser.readline() # print out connection confirmation message

    status = "off"

    while True: # keeping reading data from Arduino
        line = ser.readline() # reading serial output from Arduino line by line
        data = str.strip(line) # strip newline from the end

        if data == "start": # z button pressed down for first time
            gesture = []
            status = "on"

            step = 30 # step for how frequently to record readings
            window = 50 # window to average across
            counter = step - window # start w/ neg number to be able to use mod later

            vectors = {}
            for i in range(3):
                vectors[i] = [0]*window

            print "starting to collect data now"

        elif data == "stop": # z button had been pressed down previously, now just let go of it to end collection of data
            print "finished collecting data"
            ser.close() # close serial connection

            return gesture

        elif status == "on":
            #print "collecting data..."
            print data

            counter += 1

            values_list = str.split((data), ",") # break apart into a 3-item [x, y, z] list

            for i in range(len(values_list)):
                values_list[i] = int(values_list[i]) # convert contents of vector_list into numbers
                vectors[i].pop(0) # pop off oldest value
                vectors[i].append(values_list[i]) # append newest value

            if counter % step == 0 and counter != 0: # for taking readings at the right steps (30, 60...) but skip when counter hits 0
                reading = []

                for i in range(3):
                    avg = get_avg(vectors[i])
                    converted_value = convert_data(avg)

                    reading.append(converted_value)

                gesture.append(reading)

        else:
            ser.close()

            return "Too slow to give input, timed out!"


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

