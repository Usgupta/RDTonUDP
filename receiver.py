import pathlib
from socket import *
import sys
import time
from datetime import datetime
import secrets
import traceback
from packet import Packet

# opening all the log files and removing any previous data

expectedseq = 0 # expected packet sequence number
data_buff = [None] * 32 #data buffer list
# filename = "received.txt"
filename = sys.argv[4]


file = open(filename,"w")
file.close()

file = open("arrival.log","w")
file.close()

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
    global filename

    try:
        emulator_addr = sys.argv[1] #emulator address 014

        emulator_port = int(sys.argv[2]) #emulator port
        rec_port = int(sys.argv[3])
        
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rec_port)) 

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
    writes the data from buffer to a file. updates the expected sequence number for the next packet
    
    """
    global expectedseq
    print("writing data")
    with open(filename, mode="a") as fp:
        print("opened file")
        while data_buff[expectedseq]!=None:
            # if(data_buff)
            print("looping thru data: ", expectedseq)
            fp.write(data_buff[expectedseq])
            data_buff[expectedseq] = None
            expectedseq+=1
            expectedseq%=32
    print("finished writing data")


if __name__ == "__main__":
    main(sys.argv[1:])