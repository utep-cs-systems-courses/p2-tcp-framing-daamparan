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
    def readLine(): #reads line \ functions like input
        return os.read(0,1024).decode()

    def myPrint(self, string): #takes the string and prints onto string
        os.write(1, (string + '\n').encode())


    def myOpen(self, fileName): #open our files to be able to read them
        try:
            fd_in = os.open(fileName, os.O_RDONLY) #open and read the file
            self.rbuf = os.read(fd_in,1024)
            if len(self.rbuf) == 0:
                myPrint('File is empty')
                pass
        os.close(fd_in)#close the file

        except FileNotFoundError:
            myPrint('File was not found')
            sys.exit(1)

    def myWrite(self, fileName): #custom write to file method
        fd_out = os.open(fileName, os.O_WRONLY | os.O_CREAT) #output file descriptor | open if existing / create if not
        os.write(fd_out, self.rbuf) #writing to the file
        os.close(fd_out)


    def close(self):
        return self.sock.close()

    def send(self, fileName, payload):
        msg = str(len(payload)).encode() + b':' + fileName.encode() + b':' + payload #seperate things by total chars in the message
        while len(msg): #as we iterate thorugh the entire message
            sent = self.sock.send(msg) #attain the number of bytes transfered
            msg = msg[sent:] #split the rest of the message by those setn already


    def receive(self):
        state = 1
        msgLength = -1 #will represent the length of the message

        while True:
            if state == 1:
                msg = re.match(b'([^:]+):(.*):(.*)', self.rbuf , re.DOTALL | re.MULTILINE) #looks for the colon in the message
                if msg:
                    length, fileName, self.rbuf = msg.groups() #seperate items by :
                    try:
                        msgLength = int(length) #type cast the string\
                    except:
                        if len(self.rbuf):
                            self.myPrint('ERROR: Message length incorrect')
                            return None
                    state = 2
            if state == 2:
                if len(self.rbuf >= msgLength):
                    payload = self.rbuf[:msgLength]
                    self.rbuf = self.rbuf[msgLength:]
                    return fileName, payload
