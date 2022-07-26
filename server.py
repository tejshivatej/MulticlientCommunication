"""
Description: This file is to implement Socket Server for Multi client communication (upto 50 clients can communicate at time) 
using socket and threading modules And to store that communicated messages into tessrac database using MySQL
Author: Shivateja Kokkula
Position: Junior Software Engineer

"""


import queue # importing queue module which stores items in FIFO manner and recently added item will be removed first
import threading # importing a threading module
import socket # importing a socket module
from time import sleep # importing sleep from time


host = socket.gethostname() # Get local machine name
port = 48574 # reserve a port for your service
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a socket object with name of server
server.bind((host, port)) # bind the host with port
server.listen() # Now waiting for client connections


client_length = 0 # initiating clients_length for key generation to create a dictionary with that key
clientQ = queue.Queue() # connected clients will be added in FIFO manner


clients = {} # initializing clients to store connected clients


def router():

    """

    Description: It receives the clients connections
    
    """

    while True:
        while True:
            try:
                _client = clientQ.get_nowait()
                clients.update(dict(_client)) # adds connected clients to clients dictionary
                print(clients) # prints the clients that are connected to server
                if clientQ.empty():
                    # if clientQ is empty it prints Q empty
                    print('Q empty')
                    break
            except queue.Empty:
                break

        sleep(.5)
        try:
            for client, conn in clients.items():
                msg = conn.recv(1024).decode('utf-8')
                print(msg) # prints the received message
                if msg == "":
                    continue
                receiver, msg = msg.split(':',1) # seperates the receiver and message
                if receiver in clients:
                    # if the receiver in connected clients, then message will sent to that particular client
                    clients[receiver].send(msg.encode('utf-8'))
                    print(f"{msg} - sent to {receiver}")
                else:
                    # if the receiver not in connected clients, then it prints user not in list
                    print(f"user not in list")
        except RuntimeError:
            continue

routerThread = threading.Thread(target=router) # initiate routerThread
routerThread.start() # Running the router function
sleep(.5) # wait for .5 second

def receive():
    global client_length
    print('Server is running and listening ...') # After server starts running, it prints "Server is running and listening ..."


    while True:
        client, address = server.accept() # accepting connection
        print(f'connection is established with {str(address)}') # prints connection established with respective IP address
        msg = client.recv(1024).decode('utf-8')
        print(msg)
        if msg == 'register':
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode('utf-8')
            clientQ.put({alias:client}) # adding alias and client to clientQ
            print(f'{alias} has joined and username is - {alias}'.encode('utf-8')) # prints that registered user is joined
        else:
            receiver, msg = msg.split(':',1) # separates the receiver name and message
            # if receiver in clients, then receiver gets message
            if receiver in clients:
                clients[receiver].send(msg).encode('utf-8')
            else:
                print(f"user not in list") # if receiver not in clients, prints user not in list



if __name__ == "__main__": # allow or prevent parts of code from being run when the modules are imported
    receive() # calling receive function