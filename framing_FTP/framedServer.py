#! /usr/bin/env python3

import sys
sys.path.append("/../lib")       # for params
import re, socket, params, os
from FTP import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lSock.bind(bindAddr)
lSock.listen(5)
myPrint('Listening to: ' + str(bindAddr))

while True:
    conn, addr = lSock.accept()
    myPrint('Connected to: ' + str(addr))

    try:
        myPrint('Attempting to receive file\n')
        fileName, recBuf = ftp_Receive(conn) #calls receive method in FTP
        print(recBuf)

    except:
        myPrint('Error: Failure to transfer the file')

    if recBuf is None:
        myPrint('File is empty')
        sys.exit(1)

    fileName = fileName.decode()

    myPrint('Receiving: ' + fileName)
    myWrite(fileName, recBuf)
