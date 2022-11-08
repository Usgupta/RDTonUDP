# import imp
import pathlib
from socket import *
import sys
import time
from datetime import datetime
import secrets
import traceback
from packet import Packet
# import numpy as np


# def convert_int_to_bytes(x):
#     """
#     Convenience function to convert Python integers to a length-8 byte representation
#     """
#     return x.to_bytes(8, "big")


# def convert_bytes_to_int(xbytes):
#     """
#     Convenience function to convert byte value to integer value
#     """
#     return int.from_bytes(xbytes, "big")


# def read_bytes(socket, length):
#     """
#     Reads the specified length of bytes from the given socket and returns a bytestring
#     """
#     buffer = []
#     bytes_received = 0
#     while bytes_received < length:
#         data = socket.recv(min(length - bytes_received, 1024))
#         if not data:
#             raise Exception("Socket connection broken")
#         buffer.append(data)
#         bytes_received += len(data)

#     return b"".join(buffer)

expectedseq = 0

data_buff = [None] * 32

def sendEOT(emulator_addr, emulator_port, clientSocket, seqno):
    data = ""
    ptype = 2
    seqno += 1
    seqno=seqno%32
    lendata = 0
    packet = Packet(ptype,seqno,lendata,data)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

def sendACK(emulator_addr, emulator_port, clientSocket, seqno):
    data = ""
    ptype = 0
    # seqno += 1
    # seqno=seqno%32
    lendata = 0
    packet = Packet(ptype,seqno,lendata,data)
    print("ack packet: ", seqno)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))


def main(args):
    # port = int(args[0]) if len(args) > 0 else 4321
    # address = args[1] if len(args) > 1 else "localhost"

    

    try:

        emulator_addr = "129.97.167.47" #emulator address 010
        # emulator_addr = "129.97.167.51" #emulator address 002

        emulator_port = 6186 #emulator port
        # clientSocket = socket(AF_INET, SOCK_DGRAM)
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


            recvd_packet = Packet(serverSocket.recv(1024))
            print("got the packet")
            print(recvd_packet)

            typ, seqnum, length, data = recvd_packet.decode()
            # print("packet vals are", typ,seqnum,length,data)

            if typ==2:
                print("EOT")

                serverSocket.sendto(recvd_packet,(emulator_addr, emulator_port))

                # sendEOT(emulator_addr, emulator_port, clientSocket, len(finaldata))
                exit()
            else:
                if seqnum!=expectedseq and seqnum in range(expectedseq,expectedseq+10):
                    data_buff[seqnum] = data
                    print("check not seq expec")
                if seqnum == expectedseq:
                    print(" seq eq expec")
                    data_buff[seqnum] = data
                    print(data_buff)
                    writedata(filename, data_buff)
                print("sending ack")
                sendACK(emulator_addr,emulator_port,serverSocket,expectedseq-1)
                
                # finaldata[seqnum]=data
                # typ = 0


            # message1, clientAddress = serverSocket.recvfrom(2048) 
            # message2, clientAddress = serverSocket.recvfrom(2048) 


            # Write the file with 'recv_' prefix
                
    except Exception as e:
        print(e)

def writedata(filename, data_buff):
    global expectedseq
    print("writing data")
    with open(filename, mode="a") as fp:
        print("opened file")
        print(expectedseq)
        while data_buff[expectedseq]!=None:
            print("looping thru data: ", expectedseq)
            fp.write(data_buff[expectedseq])
            data_buff[expectedseq] = None
            expectedseq+=1

                    # fp.write(message2)
    print("finidhed")
                    # f"Finished receiving file in {(time.time() - start_time)}s!"
                # )
        # s.close()


if __name__ == "__main__":
    main(sys.argv[1:])