#! /usr/bin/env python3

import sys
sys.path.append("../../lib")       # for params
import re, socket, params, os

from threadFTP import threadSock
from threading import Thread, Lock;

def myPrint(string): #takes the string and prints onto string
    os.write(1, (string + '\n').encode())

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
progname = "threadServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']
if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

lock = Lock() #lock for the threads
files_InTrans = [] #holds what files are being transfered

#methods required to check whether the file is transfering already
def startTransfer(fileName):
    global lock, files_InTrans #allows us to edit the global vars
    lock.acquire() #lock the thread
    if fileName in files_InTrans: #if the file is already being transfered
        myPrint('Error: File is already being transfered')
        lock.release() #unlock the lock
        sys.exit(1)
    else:
        files_InTrans.append(fileName) #add the file to list
        lock.release() #unlock the lock

def endTransfer(fileName):
    global lock, files_InTrans
    lock.acquire() #lock
    files_InTrans.remove(fileName) #remove the file from the list\
    lock.release() #unlock

#class for server
class Server(Thread): #easier to operate since each obj is a thread
    def __init__(self, sockAddr):
        self.sock, self.address = sockAddr #attain socket information
        self.fsock = threadSock(sockAddr) #create threadSocket

    def run(self):
        myPrint('New thread connection from: ' + str(self.address)) #print connection
        while 1:
            try:
                myPrint('\nTrying to receive data')
                fileName, payload = self.fsock.receive() #call receive method
            except:
                myPrint('\nError: Cannot transfer file | Receiving not successful\n')
                sys.exit(1)

            if self.rbuf is None:
                myPrint('Error: File is empty\nNothing to send\n')
                sys.exit(1)

            fileName = fileName.decode()
            startTransfer(fileName)
            self.fsock.myWrite(fileName) #if the we continue then there is no error
            endTransfer(fileName) #delete file from table
            #after it is complete we close the socket
            fsock.close()

while 1:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.run()
    #after the run is complete
