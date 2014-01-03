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
#
t=""
print "Start"


# http://stackoverflow.com/a/3173331
def update_progress(progress):
	bash = (progress/5)
	space = 20 - bash
	print '\r[{0}{1}] {2}%'.format('#'*(progress/5), ' '*space, progress),


start_time = time.time()
while True:

	#for i in range(0, 256):
		#print "write"
		#ser.write(str(ord(b[a +i])) + "\n")
	ser.write(b[a:a+256])

	a = a + 256
	#for i in range(0, 4):
	#	print ser.readline()
	#print "address",

	update_progress(int(a * 1.0/0x7ffff *100.0))	
	#print (a * 1.0/0x7ffff *100.0)	

	ser.readline();

	if (a>0x7ffff):

		print "Complete!"
		# your code
		elapsed_time = time.time() - start_time
		print elapsed_time
		exit()
