# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *

serverPort = 12000
serverName = '10.10.17.95'  # '172.16.21.10' '10.10.255.254'

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind((serverName, serverPort))  # binds the socket to the given server name and port
print('The server is ready to receive messages.')

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # Receive the client packet along with the client's address
    message, address = serverSocket.recvfrom(1024)
    print('Message received from client: ')

    print(message)  # prints out received
    message = message.decode().upper()  # decodes the received message and changes the message to uppercase

    # if rand is less is than 4, we consider the packet lost and do not respond to the client
    if rand < 4:
        print('The packet was lost.')
        continue

    # otherwise, the server responds with an encoded uppercase message
    message = message.encode()
    serverSocket.sendto(message, address)  # send back to the client

    print('Message sent back to client: ')
    print(message)  # prints out the uppercase encoded message that was sent back to the client

# close the server and the program
serverSocket.close()
print('The server was closed.')
exit()
