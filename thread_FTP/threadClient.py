#! /usr/bin/env python3
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

from threadFTP import threadSock

def myPrint(string): #takes the string and prints onto string
    os.write(1, (string + '\n').encode())

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "threadClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server) #attain the ip and port
    serverPort = int(serverPort) #type cast
except:
    pass
    myPrint('Error: Cannot parse server:port')

addrFamily = socket.AF_INET #IPV4
socktype = socket.SOCK_STREAM #TCP Connection
addrPort = (serverHost, serverPort) #tuple of server

s = socket.socket(addrFamily, socktype)
if s is None: #in case socket could not be made
    myPrint('Could not open socket')
    sys.exit(1)

myPrint('Attempting connection with : ' + str(addrPort))
s.connect(addrPort)

fsock = threadSock((s, addrPort)) #create the thread socket object

while 1:
    myPrint('Enter the file you want to send') #message to attain input
    fileName = fsock.readLine() #read user input
    fileName = fileName.strip()

    fsock.myOpen(fileName) #open and read the file

    myPrint('Sending File: ' + fileName)
    fsock.send(fileName)
    fsock.close()
