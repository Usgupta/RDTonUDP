# import imp
import pathlib
from socket import *
import sys
import time
from datetime import datetime
import secrets
import traceback
from packet import Packet



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


def read_bytes(socket, length):
    """
    Reads the specified length of bytes from the given socket and returns a bytestring
    """
    buffer = []
    bytes_received = 0
    while bytes_received < length:
        data = socket.recv(min(length - bytes_received, 1024))
        if not data:
            raise Exception("Socket connection broken")
        buffer.append(data)
        bytes_received += len(data)

    return b"".join(buffer)

def sendEOT(emulator_addr, emulator_port, clientSocket, seqno):
    data = ""
    ptype = 2
    seqno += 1
    seqno=seqno%32
    lendata = 0
    packet = Packet(ptype,seqno,lendata,data)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

def main(args):
    # port = int(args[0]) if len(args) > 0 else 4321
    # address = args[1] if len(args) > 1 else "localhost"

    

    try:

        emulator_addr = "129.97.167.47" #emulator address
        emulator_port = 6186 #emulator port
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        rec_port = 52081
        # serverPort = port
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rec_port)) 
                            # If the packet is for transferring a chunk of the file
                            # start_time = time.time()

                            # file_len = convert_bytes_to_int(
                                # read_bytes(client_socket, 8)
                            # )
                            # file_data = read_bytes(client_socket, file_len)
                            # print(file_data)

        filename = "rec.txt"
        finaldata = {}

        while True:


            recvd_packet = serverSocket.recv(1024)
            print("got the packet")

            typ, seqnum, length, data = Packet(recvd_packet).decode()
            print("packet vals are", typ,seqnum,length,data)
            if typ==2:
                print("EOT")

                with open(
                    filename, mode="w"
                ) as fp:

                    for seqno, seqdata in sorted(finaldata.items()):
                        fp.write(seqdata)

                    # fp.write(message2)
                print("finidhed"
                    # f"Finished receiving file in {(time.time() - start_time)}s!"
                )
                sendEOT(emulator_addr, emulator_port, clientSocket, len(finaldata))


                exit()
            else:
                finaldata[seqnum]=data

            # message1, clientAddress = serverSocket.recvfrom(2048) 
            # message2, clientAddress = serverSocket.recvfrom(2048) 


            # Write the file with 'recv_' prefix
                
    except Exception as e:
        print(e)
        # s.close()


if __name__ == "__main__":
    main(sys.argv[1:])