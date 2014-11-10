#! /usr/bin/env python

#############################################################################
## Fu.py --- POC tool by Cameron Maerz, simply heavily edited source of    ##
## a tunneling proxy demo by  Philippe Biondi.                             ##
## source is available @ //secdev.org/python/tunproxy.py                   ##
##                                                                         ##
## Presenting!        some ugly shit by cC                                 ##
##    To bypass, evade, dos, and fubar things                              ##
##      python Fu.py -s 53 -c 10.0.0.1:80                                  ##
##         mpls network security test thing or other type dingledong       ##
##            000hh noes the cable wifi alliance                           ##
##               http://www.cablewifi.com/ for a list of providers         ##
## This program is free software; you can redistribute it and/or modify it ##
## under the terms of the GNU General Public License as published by the   ##
## Free Software Foundation; either version 2, or (at your option) any     ##
## later version.                                                          ##
##                                                                         ##
## This program is distributed in the hope that it will be useful, but     ##
## WITHOUT ANY WARRANTY; without even the implied warranty of              ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU       ##
## General Public License for more details.                                ##
##                                                                         ##
#############################################################################


import os, sys
from socket import *
from fcntl import ioctl
from select import select
import getopt, struct



TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002

TUNMODE = IFF_TUN
MODE = 0
DEBUG = 0

def usage(status=0):
    print "Usage: Fu [-s port|-c targetip:port] [-e]"
    sys.exit(status)

opts = getopt.getopt(sys.argv[1:],"s:c:ehd")

for opt,optarg in opts[0]:
    if opt == "-h":
        usage()
    elif opt == "-d":
        DEBUG += 1
    elif opt == "-s":
        MODE = 1
        PORT = int(optarg)
    elif opt == "-c":
        MODE = 2
        IP,PORT = optarg.split(":")
        PORT = int(PORT)
        peer = (IP,PORT)
    elif opt == "-e":
        TUNMODE = IFF_TAP
        
if MODE == 0:
    usage(1)


f = os.open("/dev/net/tun", os.O_RDWR)
ifs = ioctl(f, TUNSETIFF, struct.pack("16sH", "tbag%d", TUNMODE))
ifname = ifs[:16].strip("\x00")

print "w00t interface = %s" % ifname

s = socket(AF_INET, SOCK_DGRAM)

try:
    if MODE == 1:
        s.bind(("", PORT))
    print "Mushroom stamped the captive portal"     
           
    while 1:
        r = select([f,s],[],[])[0][0]
        if r == f:
            if DEBUG: os.write(1,">")
            s.sendto(os.read(f,1500),peer)
            buf,p = s.recvfrom(1500)
            if DEBUG: os.write(1,"<")
            os.write(f, buf)
except KeyboardInterrupt:
    print "Stopped by user."
