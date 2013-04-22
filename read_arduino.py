import serial

def read_arduino():
    ser = serial.Serial(port='/dev/tty.usbmodemfa131', baudrate=19200, timeout= 3) # will time out any .readline() below after 3 seconds

    print ser.readline() # print out connection confirmation message

    status = "off"

    while True: # keeping reading data from Arduino
        line = ser.readline() # reading serial output from Arduino line by line
        data = str.strip(line) # strip newline from the end

        if data == "start": # z button pressed down for first time
            gesture = []
            status = "on"
            print "starting to collect data now"

        elif data == "stop": # z button had been pressed down previously, now just let go of it to end collection of data
            print "finished collecting data"
            ser.close() # close serial connection

            return gesture

        elif status == "on":
            print "collecting data..."
            vector_list = str.split((data), ",") # break apart into a 3-item [x, y, z] list

            for i in range(len(vector_list)):
                vector_list[i] = int(vector_list[i]) # convert contents of vector_list into numbers

            gesture.append(vector_list)

        else:
            ser.close()

            return "Too slow to give input, timed out!"



def draw_gesture(vector_list):
    pass