from socket import *
import time

# resets both the start and end round-trip-time
def resetRTT():
    return (0, 0)

# determines the fastest ping time from the packets that were sent and receieved by the client
def fastestPing(arr):
    fast = arr[0]
    for element in arr:
        if element < fast:  # if the current element in the array is smaller than the ping time is faster, update fastest
            fast = element
    return fast

# determines the slowest ping time of the packets that were sent and received by the client
def slowestPing(arr):
    slow = arr[0]
    for element in arr:
        if element > slow:  # if the current element in the array is larger than the ping time is slower, update slowest
            slow = element
    return slow

# determines the average ping time of the packets that were sent and received by the client
def average(arr):
    sum = 0
    for element in arr:
        sum += element
    return sum / len(arr)


# keep track of the time
rtt_start: float = 0  # round-trip-time start
rtt_end: float = 0  # round-trip-time end
time_arr = []  # an array of all the packets pings that were successfully sent and received

serverName: str = gethostbyname('google.com')  # IP Addresses I tested with: '10.10.21.8' '172.16.21.12' '172.16.21.10' '10.10.17.95'
serverPort: int = 1337
clientSocket: socket = socket(AF_INET, SOCK_DGRAM)
sent: int = 0
timedOut: bool = False
successfullyTransmitted: int = 0

while True:
    try:
        if sent < 10:
            message: str = input('Input lowercase sentence: ')  # receive an input message from user
            rtt_start += time.time()
            clientSocket.sendto(message.encode(), (serverName, serverPort))  # attempt to send message to the server

            try:
                clientSocket.settimeout(1)  # times out after one second
                message, address = clientSocket.recvfrom(1024)  # if the server does not timeout the client receives the message
            except:
                timedOut = True
                continue

    finally:
        if sent < 10:
            sent += 1
            if not timedOut:  # if the connection did not time out proceed and display the rtt for the current ping
                successfullyTransmitted += 1
                rtt_end += time.time()
                elapsed: float = rtt_end - rtt_start
                time_arr.append(elapsed)
                if elapsed > 1:
                    print(f'Ping {sent}: {elapsed} seconds.')
                else:
                    print(f'Ping {sent}: %s milliseconds.' % (elapsed * 1000))
            else:  # otherwise the request has timed out
                print(f'Ping {sent} request timed out.')
        else:  # if the client has sent 10 pings already than stop pinging the server
            break

        rtt_start, rtt_end = resetRTT()  # reset the rtt to 0
        timedOut = False  # make sure that if the connection timed out to change the timed out flag back to false

clientSocket.close()  # close the connection from the client to the server

if not len(time_arr) == 0:  # if the client was able to send at least one ping proceed
    '''
        Give a summary of the client's performance including:
    1) The fastest ping time
    2) The slowest ping time
    3) The average ping time
    4) Percentage of packets lost
    '''
    fastest = fastestPing(time_arr)
    slowest = slowestPing(time_arr)
    avg = average(time_arr)

    if fastest < 1:
        print(f'Fastest ping time: {fastest} milliseconds')
    else:
        print(f'Fastest ping: {fastest} seconds')

    if slowest < 1:
        print(f'Slowest ping time: {slowest * 1000} milliseconds.')
    else:
        print(f'Slowest ping: {slowest} seconds.')

    if avg > 1:
        print(f'Average ping time: {avg} seconds.')
    else:
        print(f'Average ping time: {avg * 1000} milliseconds.')

    print(f'Packet loss: {(float)(10 - successfullyTransmitted)/ 10}%')

# close out the program
print('Closed connection.')
exit()
