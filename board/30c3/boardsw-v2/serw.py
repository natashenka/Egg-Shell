import serial
import time
import sys

#enter your device file
arddev = sys.argv[1]
baud = 115200

#setup - if a Serial object can't be created, a SerialException will be raised.
start_time = time.time()

while True:
    try:
        ser = serial.Serial(arddev, baud)

        #break out of while loop when connection is made
        break
    except serial.SerialException:
        print 'waiting for device ' + arddev + ' to be available'
        time.sleep(3)

#read lines from serial device
f = open(sys.argv[2], 'rb')
b = f.read()
a = 0;
print "Start"
start_time = time.time()
while True:
	ser.write(b[a:a+16])
        ser.flush()

	a = a + 16

        if (a % 256) == 0:
            print (a * 1.0/0x7ffff *100.0)

        while True:
            status_line = ser.readline().strip();
            if status_line[0] == '.':
                break
            elif status_line[0:5] == "FAIL:":
                print status_line
                print "Write failed"
                exit()
            else:
                print status_line

	if (a>0x7ffff):
		print "Complete!"
		# your code
		elapsed_time = time.time() - start_time
		print elapsed_time
		exit()
