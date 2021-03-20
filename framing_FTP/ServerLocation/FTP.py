import re, os, sys

'''
Author: David Amparan | Date: 3/17/2021
FTPSock.py is going to represent our own custom transfer protocol
Its main use is for file transfer from the Client to Server
It should be taking in user input which is a file name, transfer its data
and then the Server will create the file and copy the data into it
Here we will simply define the send and recv of our
protocol
'''
#below are copied from the previous iteration
def readLine(): #reads line \ functions like input
    return os.read(0,1024).decode()

def myPrint(string): #takes the string and prints onto string
    os.write(1, (string + '\n').encode())

def myOpen(fileName): #open our files to be able to read them
    try:
        fd_in = os.open(fileName, os.O_RDONLY) #open and read the file
        rBuf = os.read(fd_in,1024)
        if len(rBuf) == 0:
            myPrint('File is empty')
            pass
        os.close(fd_in)#close the file

        return rBuf #buffer of what has been read
    except FileNotFoundError:
        myPrint('File was not found')
        sys.exit(1)

def myWrite(fileName, wBuf): #custom write to file method
    fd_out = os.open(fileName, os.O_WRONLY | os.O_CREAT) #output file descriptor | open if existing / create if not
    os.write(fd_out, wBuf) #writing to the file
    os.close(fd_out)

def ftp_send_Hello(sock): #intial send of the socket | Greeting to the Client
    sock.send(('Hello World').encode()) #send greet
    sock.send('.'.encode())

def ftp_Send(sock, fileName, payload):
    #format x:fileName:message
    msg = str(len(payload)).encode() + b':' + fileName.encode() + b':' + payload #seperate things by total chars in the message
    while len(msg): #as we iterate thorugh the entire message
        sent = sock.send(msg) #attain the number of bytes transfered
        msg = msg[sent:] #split the rest of the message by those setn already

receivebuf = b'' #global rbuf
def ftp_Receive(sock):
    global receivebuf #allows us to edit the receivebuf
    messageLen = -1 #length of the message received
    stage = 1

    while True:
        if stage == 1: #stage acts like states
            msg = re.match(b'([^:]+):(.*):(.*)', receivebuf, re.DOTALL | re.MULTILINE) #looks for the colon in the message
            if msg:
                length, fileName, receivebuf = msg.groups() #seperate items by :
                try:
                    messageLen = int(length) #try to convert integer
                except:
                    if len(receivebuf):
                        print('Message length not in correct format')
                        return None, None
                stage = 2 #now we attain the payload
        #print(len(receivebuf))
        #print(messageLen)
        if stage == 2:
            if len(receivebuf) >= messageLen: #if they do not match
                payload = receivebuf[0:messageLen]
                receivebuf = receivebuf[messageLen:]
                return fileName, payload #return what is read

        rev = sock.recv(1024)#receive 1024 bytes
        receivebuf = receivebuf + rev #add to the received buffer
        if len(receivebuf) == 0: #there is nothing to do
            if len(receivebuf) != 0: #if there is a message in the buffer
                print('Message is not complete')
            return None
