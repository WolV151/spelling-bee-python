import socket

# pretty much copied from the examples folder on github

SERVER = "0.0.0.0" # assuming the server is running in a docker container on the local machine
PORT = 64001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes("This is from Client", 'UTF-8'))

while True:
    in_data = client.recv(1024)
    print("From Server :", in_data.decode())  # print the stats sent from server
    

client.close()