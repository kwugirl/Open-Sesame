import serial
ser = serial.Serial('/dev/tty.usbmodemfa131', 19200)
print ser.readline() # to print the connection confirmation message

gesture = []


while len(gesture) < 10:
    data = ser.readline() # reading serial output from Arduino line by line
    # print data
    vector = str.strip(data) # strip newline from the end
    vector_list = str.split((vector), ",") # break apart into a 3-item [x, y, z] list

    # print "this is the line before numerical conversion", vector_list

    for i in range(len(vector_list)):
        vector_list[i] = int(vector_list[i]) # convert contents of tuple into numbers

    # print "this is the line after numerical conversion", vector_list

    gesture.append(vector_list)

print gesture # list of lists of xyz coordinates