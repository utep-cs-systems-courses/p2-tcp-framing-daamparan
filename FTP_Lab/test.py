#! /usr/bin/env python3
import os

def readLine():
    return os.read(0,1024).decode()

def myPrint(string):
    os.write(1, (string + '\n').encode())

def myOpen(fileName):
    fd_in = os.open(fileName, os.O_RDWR | os.O_CREAT) #open and read the file
    #os.set_inheritable(0, True) #change the file descriptor input
    myPrint((os.read(fd_in,1024)).decode())
    os.close(fd_in)

def myWrite(fileName, wBuf):
    fd_out = os.open(fileName, os.O_WRONLY | os.O_CREAT)
    os.write(fd_out, wBuf.encode())
    os.close(fd_out)

#t = readLine()
#r = readLine()
#myOpen(t[:t.index('\n')])
#myWrite(r[:r.index('\n')], 'My new string file')
t = readLine()
myOpen(t[:t.index('\n')])


'''
while '\n' in t:
    myPrint(t[:t.index('\n')])
    t = t[t.index('\n') + 1:]
'''
