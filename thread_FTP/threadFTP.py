'''
Author: David Amparan | Date: 3/25/2021
threadFTPSock.py is going to represent our own custom transfer protocol using threads
Its main use is for file transfer from the Client to Server
It should be taking in user input which is a file name, transfer its data
and then the Server will create the file and copy the data into it
Here we will simply define the send and recv of our
protocol

To ease the use of threads we will create a class
for the threaded socket to avoid confusing by mixing threads with method handling
Furthermore, many of the methods found here are copied and pasted from the other FTPSock file
which can be found in the other folders
'''
import re

class threadSock:
    def __init__(self, sockAddr):
        self.sock, self.addr = sockAddr #attain the socket information
        self.rbuf - b"" #replaces global read buffer

     #further methods
    def close(self):
        return self.sock.close()

    def send(self, fileName, payload):
        msg = str(len(payload)).encode() + b':' + fileName.encode() + b':' + payload #seperate things by total chars in the message
        while len(msg): #as we iterate thorugh the entire message
            sent = sock.send(msg) #attain the number of bytes transfered
            msg = msg[sent:] #split the rest of the message by those setn already

        receivebuf = b'' #global rbuf

    def receive(self):
        state = 1
        msgLength = -1 #will represent the length of the message

        while True:
            if state == 1:
                msg = re.match(b'([^:]+):(.*):(.*)', self.rbuf , re.DOTALL | re.MULTILINE) #looks for the colon in the message
                if msg:
                    length, fileName, rbuf = msg.groups() #seperate items by :
                    try:
                        msgLength = int(length) #type cast the string\
                    except:
                        if len(rbuf):
                            #add my print method here
                            return None, None
