import socket
import threading

import json
import sys
import os
import pika


my_messages = []

"""
I tried running the server normally inside the docker, but I had no idea how to set up rabbitmq
and it crashed everytime because the server which is the consumer, running in the container,
couldn't see the spelling bee server which is the producer.

In the end I used the option --network="host" which allowed everything to message eachother because the container's
network stack was not isolated from my machine
"""
# The server is taken from the examples folder on github

class ClientThread(threading.Thread):

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)


    def callback(self, ch, method, properties, body): # callback, I send the stats to the client here
        print(f"Message Received: {json.loads(body)}")
        my_messages.append(f"Message Received: {json.loads(body)}")
        self.c_socket.send(bytes(f"Message Received: {json.loads(body)}", 'UTF-8'))



    def run(self):
        print("Connection from : ", clientAddress)
        while True: # run rabbitmq consumer
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
            channel = connection.channel()
            channel.queue_declare('games_stats')
            channel.basic_consume(queue='games_stats', auto_ack=True , on_message_callback=self.callback)

            print("Connection established. Waiting for messages. Press CTRL+C to interrupt.")
            channel.start_consuming()

        print("Client at ", clientAddress, " disconnected...")


LOCALHOST = "0.0.0.0"  # assuming it is running in a docker container
PORT = 64001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

counter = 0

while True:
    server.listen(1)
    my_socket, clientAddress = server.accept()
    counter = counter + 1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.start()