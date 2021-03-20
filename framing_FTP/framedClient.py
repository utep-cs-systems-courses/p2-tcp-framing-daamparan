#! /usr/bin/env python3

import socket, os, sys, re
sys.path.append('../lib')
import params
from FTP import *

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present) #no functionality has been given to switchesVarDefaults besides server
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = 'framedClient'
paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server) #attain the ip and port
    serverPort = int(serverPort) #type cast
except:
    pass
    myPrint('Cannot parse server:port from %s' %server)

addrFamily = socket.AF_INET #IPV4
socktype = socket.SOCK_STREAM #TCP Connection
addrPort = (serverHost, serverPort) #tuple of server

s = socket.socket(addrFamily, socktype) #create the socket

if s is None: #in case socket could not be made
    myPrint('Could not open socket')
    sys.exit(1)

s.connect(addrPort)
while 1:
    myPrint('Enter the file you want to send') #message to attain input
    fileName = readLine() #read user input
    read = myOpen(fileName.strip()) #open the file name

    myPrint('Sending file')
    ftp_Send(s, fileName, read) #method to send the file
