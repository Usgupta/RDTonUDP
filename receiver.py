import pathlib
from socket import *
import sys
import time
from datetime import datetime
import secrets
import traceback
from packet import Packet

# opening all the log files and removing any previous data
file = open("rec.txt","w")
file.close()

file = open("arrival.log","w")
file.close()

expectedseq = 0 # expected packet sequence number
 
data_buff = [None] * 32 #data buffer list

def sendEOT(emulator_addr, emulator_port, clientSocket, seqno):
    """
    takes in the ip address, port number socket and packet sequence number to send the EOT packet 
    """
    data = ""
    ptype = 2
    seqno += 1
    seqno=seqno%32
    lendata = 0
    packet = Packet(ptype,seqno,lendata,data)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

def sendACK(emulator_addr, emulator_port, clientSocket, seqno):
    """
    takes in the ip address, port number socket and packet sequence number to send the ACK for a packet 
    """
    data = ""
    ptype = 0
    lendata = 0
    packet = Packet(ptype,seqno,lendata,data)
    print("ack packet: ", seqno)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

def logpacket(seqnum):
    """
    takes in the packet sequence number and writes to arrival.log file to record the arrived packet sequence number 
    """
    with open("arrival.log", mode="a") as fp:
        print("opened log file")
        fp.write(str(seqnum) + "\n")

def main(args):

    try:
        emulator_addr = "129.97.167.46" #emulator address 014

        # emulator_addr = "129.97.167.47" #emulator address 010
        # emulator_addr = "129.97.167.51" #emulator address 002

        emulator_port = 1037 #emulator port
        rec_port = 52081
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rec_port)) 

        filename = "rec.txt"

        while True:
            recvd_packet = Packet(serverSocket.recv(1024))
            print("got a packet numbered: ", recvd_packet.seqnum)

            typ, seqnum, length, data = recvd_packet.decode() #retrieve packet values
            logpacket(seqnum) #log received packet seq no

            if seqnum==expectedseq: 
                print("got expected packet...",seqnum)

                #if received packet is EOT send back an EOT packet and exit 
                if typ==2:
                    print("EOT")
                    serverSocket.sendto(recvd_packet.encode(),(emulator_addr, emulator_port))
                    exit()
                else:
                    print(" seq eq expec")
                    data_buff[seqnum] = data #add data to buffer
                    # print(data_buff)
                    writedata(filename, data_buff) #write data to file
                    sendACK(emulator_addr,emulator_port,serverSocket,expectedseq-1) #send ACK

            else:
                print("i expected packet - ", expectedseq, "got instead - ", seqnum)

                if seqnum in range(expectedseq,expectedseq+10):
                    data_buff[seqnum] = data
                    print("adding the pac to buffer")
                sendACK(emulator_addr,emulator_port,serverSocket,expectedseq)
                                
    except Exception as e:
        print(e)

def writedata(filename, data_buff):
    """
    
    """
    global expectedseq
    print("writing data")
    with open(filename, mode="a") as fp:
        print("opened file")
        # print("my expected seq is: ",expectedseq)
        while data_buff[expectedseq]!=None:
            # if(data_buff)
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