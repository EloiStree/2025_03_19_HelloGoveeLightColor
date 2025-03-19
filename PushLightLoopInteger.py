import socket
import struct
import time

# UDP target configuration
UDP_IP = "127.0.0.1"
PORT = 7000
SLEEP_TIME = 3

while True:
    integer = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(700,710):
        integer = struct.pack('<i', i)
        sock.sendto(integer, (UDP_IP, PORT))
        print("Sent: ", i)
        time.sleep(SLEEP_TIME)
    sock.close()