import serial

# this is the driver to get data off the device (Arduino + Wii nunchuck)


def read_arduino():
    ser = serial.Serial(port="/dev/tty.usbmodemfd121", baudrate=19200, timeout= 3) # will time out any .readline() below after 3 seconds

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
                    sum = 0
                    for num in vectors[i]:
                        sum += num
                    avg = sum / len(vectors[i])

                    reading.append(avg)

                gesture.append(reading)

        else:
            ser.close()

            return "Too slow to give input, timed out!"

