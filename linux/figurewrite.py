#!/usr/bin/env python

import usb.core
import usb.util
import sys
from time import *

#find our device
dev = usb.core.find(idVendor=0x03eb, idProduct=0x7777)

#was it found?
if dev is None:
   raise ValueError('Device not found')

for configuration in dev:
   for interface in configuration:
       ifnum = interface.bInterfaceNumber
       if not dev.is_kernel_driver_active(ifnum):
           continue
       try:
           print "detach kernel driver from device %s: interface %s" % (dev, ifnum)
           dev.detach_kernel_driver(ifnum)
       except usb.core.USBError, e:
           pass

#set the active configuration. with no args we use first config.
dev.set_configuration()

usb.util.claim_interface(dev, 0)

#datapack=0x40,0,0      # change this to vary the movement  
#bytesout=dev.ctrl_transfer(0x40, 6, 0x100, 0, datapack, 1000)  

#print "h"
#ret = dev.ctrl_transfer(0x80, 0x00, 0x00, 0x00, [0x47, 0x4D, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00])
#msg = 'test'
sleep(1)
p = 0
f = open(sys.argv[1], 'rb')
b = f.read()
a = 0;
while (True):

                t = []
                for i in range(0, 8):
                        t.append(ord(b[a +i]))
               # ret = dev.ctrl_transfer(0x21, 0x09, 0 , 8, [0]+t)
                #dev.write(0x81,  [0] + t)
		print a
                dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x02, wIndex=0x00, data_or_wLength=[0]+t, timeout=100)
		a = a + 8
                #print "write"
                if(a % (256) == 0):
                      sleep(0.2)
                if(a % (256*256) == 0):
                      sleep(1)       
                if(a == 256):
                      sleep(1)
                        
                     # dev.ctrl_transfer(bmRequestType=0xa1, bRequest=0x01, data_or_wLength=2, timeout=1000)
                                           
#print dev.read(0x81, 8);
#         while(w):
               #                 a=a
             #w = 1
                #        print dev.read(0x81, 1)
                 #       print "read"

                if(a % (0x1000) == 0):

                        print (int(float(a)/0x7ffff*100)),
                        print "percent complete"

#a = dev.ctrl_transfer(0x80, 0, 0, 0, 8)
#print "here"
#print a
#msg = "test1234"
#ret = dev.ctrl_transfer(0x82, 0, 0, 0, len(msg))
#sret = ''.join([chr(x) for x in ret])
