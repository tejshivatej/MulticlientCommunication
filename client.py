"""
Description: This file is to implement Socket Client for Multi client communication (upto 50 clients can communicate at time) 
using socket and threading modules
Author: Shivateja Kokkula
Position: Junior Software Engineer

"""


import threading # importing threading module
import socket # importing socket module
import datetime # importing datetime to get datetime when client sent the message to respective client
import random # importing random to generate random id, when messages are inserted into communication table in tessrac database
import mysql.connector # importing mysql connector to connect with root mysql
from time import sleep # importing sleep from time

#  connecting to tessrac database in mysql using imported mysql.connector
con = mysql.connector.connect(host="localhost", user="root",password="Jagson@5355" ,database="tessrac")
cur = con.cursor() # using cursor for row by row processing

alias = input('Your good name: ') # taking username as a input from the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket object with name of client
h = socket.gethostname() # getting local machine name
client.connect((h, 48574)) # connect host with reserved port number


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8') # receives message from client
            if message == "alias?":
                client.send(alias.encode('utf-8')) # encode the name of user
            else:
                print(message) # prints message
        except:
            print('Error!') # prints Error!
            client.close() # close the socket when done
            break


def client_send():
    OneTimeFlag = True # initiate onetimeflag as True
    while True:
        if OneTimeFlag is True:
            client.send(b'register') # client will be registered
            OneTimeFlag = False # once the client was registered, Change onetimeflag to false to decrease duplicate clients
        msg = input() # taking the message that wants to send from the user
        receiver, msg = msg.split(':',1) # seperate receiver name and message
        client.send(msg.encode('utf-8')) # encoding the message and send

        num = random.randint(5,5000) # generating random number to use as id in communication table
        date_time = datetime.datetime.now() # taking present datetime
        # query to insert the messages which are sent to respective client in communication table which is in tessrac database
        query = "Insert into communication values ({},'{}','{}','{}',1,'{}','{}')".format(num,msg,date_time,date_time,alias,receiver)
        cur.execute(query) # executing the query
        con.commit() # commit the changes that you have done on table


receive_thread = threading.Thread(target=client_receive) # initiating receive_thread
receive_thread.start() # Running the client_receive function using Thread
sleep(.2) # wait for .2 seconds

send_thread = threading.Thread(target=client_send) # initiating send_thread
send_thread.start() # Running the client_receive function using Thread
sleep(.2) # wait for .2 seconds
