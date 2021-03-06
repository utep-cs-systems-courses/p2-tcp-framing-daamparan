#! /usr/bin/env python3
'''
Author: David Amparan | Date: 3/3/2021

FTPSock.py is going to represent our own custom transfer protocol
Its main use is for file transfer from the Client to Server
It should be taking in user input which is a file name, transfer its data
and then the Server will create the file and copy the data into it

Here we will simply define the send and recv of our
protocol
'''
import re, os, sys

def readLine(): #reads line \ functions like input
    return os.read(0,1024).decode()

def myPrint(string): #takes the string and prints onto string
    os.write(1, (string + '\n').encode())

def myOpen(fileName): #open our files to be able to read them
    fd_in = os.open(fileName, os.O_RDWR) #open and read the file
    myPrint((os.read(fd_in,1024)).decode())
    os.close(fd_in)    

def ftp_send(sock, fileName): #socket gives us all the necessary information
    fileName = open(fileName, 'rb') #allows to open binary files
    file_Cont = fileName.read() #read contents
    while file_Cont:
        print(file_Cont.readLine())
        file_Cont = file_Cont.readLine()
