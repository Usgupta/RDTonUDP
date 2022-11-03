from socket import *
from random import *
import sys
import pathlib


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

emulator_addr = "129.97.167.51" #emulator address
emulator_port = 9991 #emulator port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sender_port = 9992
clientSocket.bind(('', sender_port)) 

# print(sender_port)



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
clientSocket.sendto(filename_bytes,(emulator_addr, emulator_port))

# Send the file
with open(filename, mode="rb") as fp:
    data = fp.read()
    # s.sendall(convert_int_to_bytes(1))
    # s.sendall(convert_int_to_bytes(len(data)))
    # s.sendall(data)
    clientSocket.sendto(data,(emulator_addr, emulator_port))


# message = "hello"
# clientSocket.sendto(message.encode(),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()