#! /usr/bin/env python3
'''
Author: David Amparan | Date: 3/6/2021

FTPClient.py will act as the clint connecting to the
FTPServer.py
The Client will send a file that the server must copy, the name
is then attaned from either one
'''
import socket, sys, re
sys.path.append("../lib")# for params
import params
from FTPSock import * #holds our File transfer protocol

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present) #no functionality has been given to switchesVarDefaults besides server
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
progname = 'FTPClient'
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server) #attain ip and port #
    serverPort = int(serverPort) #type cast
except: #error case
    pass
    myPrint('Cannot parse server:port from %s' %server)

addrFamily = socket.AF_INET #IPV4
socktype = socket.SOCK_STREAM #TCP COnnection
addrPort = (serverHost, serverPort) #tuple of server

s = socket.socket(addrFamily, socktype) #create the socket

if s is None: #in case socket could not be made
    myPrint('Could not open socket')
    sys.exit(1)

s.connect(addrPort)
while 1:
    try: #establish connection
        rcMsg = s.recv(1024)#receive welcome message
        if 'Hello' in rcMsg.decode(): #
            myPrint(rcMsg.decode() + '\n')

        myPrint('Enter the file that you want to send')
        fCopy = readLine() #file to copy
        myPrint('\nEnter the new file name or file name to be overwritten')
        fNewName = readLine() #new name for the file
        myPrint('\nSending file Contents')

        ftp_send(s, fNewName[:fNewName.index('\n')], fCopy[:fCopy.index('\n')]) #pass the socket, file to copy, and new name for file to be copied
    except:
        myPrint('Could not communicate')
        sys.exit(1)

#s.close() #close the socket
