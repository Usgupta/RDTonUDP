from socket import *
from random import *
import sys
import pathlib
import time
import math

from packet import Packet

import threading

from socket import *

seqnumlog = "seqnum.log"
acklog = "ack.log"
Nlog = "N.log"

lock = threading.Lock()
timestamp = 0
windowsize = 1
send_base = 0 #last ack pack
nextseqnum = 0 #latest unesent
rcvEOT = False
sentEOT = False


MAXN = 10


alllogfiles = [seqnumlog,acklog,Nlog]
for i in range(3):
    file = open(alllogfiles[i],"w")
    if alllogfiles[i]=="N.log":
        file.write(str(timestamp) + " " + str(windowsize) + "\n")
    file.close()

def addlog(file_name,data):
    with open(file_name, mode="a") as fp:
        print("opened file ",file_name)
        fp.write(str(timestamp) + " " + str(data) + "\n")
# def sendEOT(emulator_addr, emulator_port, clientSocket, seqno):
#     data = ""
#     ptype = 2
#     seqno += 1
#     seqno=seqno%32
#     lendata = 0
#     packet = Packet(ptype,seqno,lendata,data)
#     clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

# MAXREADSIZE = 500
emulator_addr = "129.97.167.46" #emulator address 014

# emulator_addr = "129.97.167.47" #emulator address 010
# emulator_addr = "129.97.167.51" #emulator address 002
emulator_port = 14836 #emulator port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sender_port = 2658
clientSocket.bind(('', sender_port)) 

# print(sender_port)
all_processes = []


# integer type; # // 0: ACK, 1: Data, 2: EOT
# integer seqnum; # // Modulo 32
# integer length; # // Length of the String variable ‘data’ // String with Max Length 500
# String data;

filename = "longtest.txt"

# while filename != "-1" and (not pathlib.Path(filename).is_file()):
#     filename = input("Invalid filename. Please try again:").strip()

# if filename == "-1":
#     s.sendall(convert_int_to_bytes(2))
#     break

# filename_bytes = bytes(filename, encoding="utf8")

# Send the filename
# clientSocket.sendto(filename.encode(),(serverName, serverPort))
# s.sendall(convert_int_to_bytes(0))
# s.sendall(convert_int_to_bytes(len(filename_bytes)))
# clientSocket.sendto(filename_bytes,(emulator_addr, emulator_port))
lastACK = False

with open(filename, mode="r") as fp:
    data = fp.read()

# Send the file
# readptr 
pacseqno = -1
readptr = 0
packets = [None] * 32
MAXPACKETS = math.ceil(len(data)/500)
MAXPACKETS%=32
print("maxpac",MAXPACKETS)

def makePackets():
    global pacseqno
    global sentEOT
    print("I am updating packets .....")
    global readptr
    if len(data)>500:
        while(readptr<=len(data)):
            if(len(packets)==32 and packets.count(None) == 0):
                break
            pacseqno += 1
            pacseqno%=32
            ptype = 1
            lendata = len(data[readptr:min(readptr+500,len(data))])
            if lendata==0:
                pacseqno += 1
                pacseqno%=32
                ptype = 2
                lendata = 0
                packets[pacseqno] = Packet(ptype,pacseqno,lendata,"")
                sentEOT = True
                print("seqno of EOT is:", pacseqno)
                pacseqno = None
                break


            # print(readptr)
            # print(data[readptr:min(readptr+500,len(data))])
            packet = Packet(ptype,pacseqno,lendata,data[readptr:min(readptr+500,len(data))])
            packets[pacseqno] = packet
            readptr+=500
    else:
        packets[0] = packet(1,0,len(data),data)
    print("val of the cond")
    print((pacseqno!=None and (readptr>len(data) or len(data)<500)))
    print((readptr>len(data) or len(data)<500))
    

    if ((readptr>len(data) or len(data)<500)):
        if pacseqno!=None:
            pacseqno += 1
            pacseqno%=32
            ptype = 2
            lendata = 0
            packets[pacseqno] = Packet(ptype,pacseqno,lendata,"")
            sentEOT = True
            print("seqno of EOT is:", pacseqno)
            pacseqno = None

makePackets() #execute it once intially to initialise the packets list

def sendPackets():
    print("I want to send some pac ...")
    print(threading.currentThread())
    print("send threads")

    # print("send p is being invoked")
    global nextseqnum
    global send_base
    global windowsize
    global timestamp
    global rcvEOT
    global sentEOT

    while True:
        if (nextseqnum-send_base)<windowsize and packets[nextseqnum]!=None:
            print("try acq lock send")
            lock.acquire()
            print("Sending packet, ", nextseqnum)
            timestamp += 1
            if lastACK:
                if packets[nextseqnum].typ==2: 
                    addlog(seqnumlog,"EOT") #add EOT to seq log
                    print("sending eot")
                    clientSocket.sendto(packets[nextseqnum].encode(),(emulator_addr, emulator_port))
                    nextseqnum += 1
                    nextseqnum= nextseqnum%32
            else:
                if packets[nextseqnum].typ!=2:
                    clientSocket.sendto(packets[nextseqnum].encode(),(emulator_addr, emulator_port))
                    addlog(seqnumlog,packets[nextseqnum].seqnum) #add seq num to seq log
                    nextseqnum += 1
                    nextseqnum= nextseqnum%32
                else:
                    print("its an eot but cant send rn")

            
        # newsendPacketThread = threading.Thread(target=sendPackets)
        # newsendPacketThread.start()
            lock.release()
            if rcvEOT:
            # print(nextseqnum,send_base)
                print("killing sending packets")
                sys.exit()
        else:
            if rcvEOT:
            # print(nextseqnum,send_base)
                print("killing sending packets")
                sys.exit()
                
            print("cant send sleeping....",rcvEOT)
            print(windowsize,send_base,nextseqnum)

            time.sleep(0.01)


    # if dup:
        
# filepackets = makePackets(filename)

dupcount = 0

def recAck():

    print("I am waiting for ack ...")
        # print("I want to send some pac ...")
    print(threading.currentThread())
    print("ack threads")

    global nextseqnum
    global send_base
    global windowsize
    global timestamp
    global dupcount
    global rcvEOT
    global lastACK
    global pacseqno
# threading.Timer(timeout, func,)
    while True:
        recvd_packet = Packet(clientSocket.recv(1024))
        if recvd_packet:
            print("try acq lock rec")

            lock.acquire()
            timestamp+=1
            print("Received ack for .......", recvd_packet.seqnum)
            # print(recvd_packet)
            
            if recvd_packet.typ == 2:
                print("got eot from rec")
                addlog(acklog,"EOT")
                # addlog(acklog,)
                clientSocket.close()
                rcvEOT = True
                sys.exit()
            else:
                addlog(acklog,recvd_packet.seqnum) #add seq num to seq log
                if recvd_packet.seqnum == send_base:
                    print("ack and rec until here: ", send_base)
                    packets[:send_base+1]= [None] * len(packets[:send_base+1])
                    send_base += 1
                    send_base %= 32
                    windowsize = min(windowsize+1,MAXN)
                    addlog(Nlog,windowsize)
                    makePackets()
                    if packets.count(None)==31 and pacseqno == None:
                        print("i hv got the last ack")
                        lastACK=True
                elif recvd_packet.seqnum == send_base - 1 and dupcount < 3:
                    print("dup inc")
                    dupcount += 1
                elif dupcount == 3:
                    print("retransmitting.....")
                    clientSocket.sendto(packets[send_base].encode(),(emulator_addr, emulator_port))
                    windowsize = 1
                    addlog(Nlog,windowsize)
                    dupcount=0
                print("release rec lock")
                lock.release()
        else:
            print("didnt rec sleeping....")
            time.sleep(0.01)
        

    #new ack inc N restart timer 
    #dup ack retrans inc timer
    # newrecAckThread = threading.Thread(target=recAck)
    # newrecAckThread.start()
    
        #restart timer


# def makePackets(seqnumlog, addlog, emulator_addr, emulator_port, clientSocket, filename, seqno):
#     with open(filename, mode="r") as fp:
#         data = fp.read()
#         if len(data)>500:
#             for i in range(0,len(data),500):
#             # print(type(data))
#                 ptype = 1
#                 seqno+=1
#                 seqno=seqno%32
#                 lendata = len(data[i:min(i+500,len(data))])
#                 print(i)
#                 print(data[i:min(i+500,len(data))])
#                 packet = Packet(ptype,seqno,lendata,data[i:min(i+500,len(data))])
#                 clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))
#                 addlog(seqnumlog,seqno) #add seq num to seq log
#                 recvd_packet = clientSocket.recv(1024)
#                 print(recvd_packet)

#         else:
#             seqno+=1
#             seqno=seqno%32
#             packet = Packet(1,seqno,len(data),data)
#             clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))
#             recvd_packet = clientSocket.recv(1024)
#             print(recvd_packet)
#     return seqno

# seqno = makePackets(seqnumlog, addlog, emulator_addr, emulator_port, clientSocket, filename, seqno)

#send EOT

# sendEOT(emulator_addr, emulator_port, clientSocket, seqno)
# print("rec pack")
# recvd_packet = clientSocket.recv(1024)
# print(recvd_packet)
# typ, seqnum, length, data = Packet(recvd_packet).decode()
 
# if __name__ == '__main__':

print("Starting sender.....")
# while not sentEOT:
sendPacketThread = threading.Thread(target=sendPackets)
recAckThread = threading.Thread(target=recAck)
sendPacketThread.start()
recAckThread.start()

# while sendPacketThread.is_alive():
#     print("sendp is alive")
# # sendPacketThread.join()
# while recAckThread.is_alive():
#     print("reck is alive")
# recAckThread.join()
