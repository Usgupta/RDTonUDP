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

file = open("rec.txt","w")
file.close()

file = open("arrival.log","w")
file.close()

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

def logpacket(seqnum):
    with open("arrival.log", mode="a") as fp:
        print("opened log file")
        fp.write(str(seqnum) + "\n")

def main(args):
    # port = int(args[0]) if len(args) > 0 else 4321
    # address = args[1] if len(args) > 1 else "localhost"

    

    try:
        # emulator_addr = "129.97.167.46" #emulator address 014

        # emulator_addr = "129.97.167.47" #emulator address 010
        emulator_addr = "129.97.167.51" #emulator address 002

        emulator_port = 1037 #emulator port
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
            print("got a packet ", recvd_packet.seqnum)
            # print(recvd_packet.seqnum)

            typ, seqnum, length, data = recvd_packet.decode()
            logpacket(seqnum)

            # print("packet vals are", typ,seqnum,length,data)
            if seqnum==expectedseq: 
                print("got expected packet...",seqnum)

                if typ==2:
                    print("EOT")
                    print(recvd_packet)

                    serverSocket.sendto(recvd_packet.encode(),(emulator_addr, emulator_port))

                    # sendEOT(emulator_addr, emulator_port, clientSocket, len(finaldata))
                    exit()
                else:
                    print(" seq eq expec")
                    data_buff[seqnum] = data
                    # print(data_buff)
                    writedata(filename, data_buff)
                    sendACK(emulator_addr,emulator_port,serverSocket,expectedseq-1)


            else:
                print("i expected packet - ", expectedseq, "got instead - ", seqnum)

                if seqnum in range(expectedseq,expectedseq+10):
                    data_buff[seqnum] = data
                    print("adding the pac to buffer")
                sendACK(emulator_addr,emulator_port,serverSocket,expectedseq)
                # print("sending ack")
                
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
        # print("my expected seq is: ",expectedseq)
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