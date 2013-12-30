import serial
import time
import sys

#enter your device file
arddev = sys.argv[1]
baud = 115200

if not arddev:
	exit("Please specify a serial port")

#setup - if a Serial object can't be created, a SerialException will be raised.
start_time = time.time()

while True:
    try:
	print "initializing serial output"
        ser = serial.Serial(arddev, int(baud), timeout=1)
	ser.flushOutput()
	print " port used: "
	print ser.portstr 
        #break out of while loop when connection is made
        break
    except serial.SerialException:
        print 'waiting for device ' + arddev + ' to be available'
        time.sleep(3)

#read lines from serial device
f = open(sys.argv[2], 'rb')
b = f.read()
a = 0
#
t=""
print "Start"
start_time = time.time()


while True:
	#for i in range(0, 256):
	#	#print "write"
	#	#ser.write(str(ord(b[a +i])) + "\n")
	ser.flushOutput()
	ser.write(b[a:a+256])

	a = a + 256
	#for i in range(0, 4):
	#	print ser.readline()
	#print "address",

	print (a * 1.0/0x7ffff *100.0)	
	while True:
		if ser.inWaiting() > 0:
			print(ser.readline())
			break

	if (a>0x7ffff):

		print "Complete!"
		# your code
		elapsed_time = time.time() - start_time
		print elapsed_time
		exit()
