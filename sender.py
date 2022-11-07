from socket import *
from random import *
import sys
import pathlib

from packet import Packet


from socket import *


def convert_int_to_bytes(x):
    """
    Convenience function to convert Python integers to a length-8 byte representation
    """
    return x.to_bytes(8, "big")


def convert_bytes_to_int(xbytes):
    """
    Convenience function to convert byte value to integer value
    """
    return int.from_bytes(xbytes, "big")



MAXREADSIZE = 500

emulator_addr = "129.97.167.47" #emulator address 010
emulator_port = 14836 #emulator port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sender_port = 2658
clientSocket.bind(('', sender_port)) 

# print(sender_port)


# integer type; # // 0: ACK, 1: Data, 2: EOT
# integer seqnum; # // Modulo 32
# integer length; # // Length of the String variable ‘data’ // String with Max Length 500
# String data;

filename = "test.txt"

while filename != "-1" and (not pathlib.Path(filename).is_file()):
    filename = input("Invalid filename. Please try again:").strip()

# if filename == "-1":
#     s.sendall(convert_int_to_bytes(2))
#     break

filename_bytes = bytes(filename, encoding="utf8")

# Send the filename
# clientSocket.sendto(filename.encode(),(serverName, serverPort))
# s.sendall(convert_int_to_bytes(0))
# s.sendall(convert_int_to_bytes(len(filename_bytes)))
# clientSocket.sendto(filename_bytes,(emulator_addr, emulator_port))
seqno = -1

# Send the file
with open(filename, mode="rb") as fp:
    data = fp.read(MAXREADSIZE).decode()
    # print(type(data))

    ptype = 1
    seqno+=1
    seqno=seqno%32
    lendata = len(data)
    packet = Packet(ptype,seqno,lendata,data)
    # print(type(packet.encode()))

    # s.sendall(convert_int_to_bytes(1))
    # s.sendall(convert_int_to_bytes(len(data)))
    # s.sendall(data)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

#send EOT
data = ""
ptype = 2
seqno += 1
seqno=seqno%32
lendata = 0
packet = Packet(ptype,seqno,lendata,data)
clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))
# message = "hello"
# clientSocket.sendto(message.encode(),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()