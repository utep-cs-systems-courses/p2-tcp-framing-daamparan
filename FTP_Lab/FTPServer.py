#! /usr/bin/env python3
'''
Author: David Amparan | Date: 3/6/2021

FTPServer.py represents the destination server within
our file transfer protocol. It will receive the messages from the
client and create a new file or update an old file if it exists
already.
'''
import re, os, sys
import socket
sys.path.append("../lib")# for params
import params
from FTPSock import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)
debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lSock.bind(bindAddr)

lSock.listen()
myPrint('Connecting to ' + str(bindAddr))
