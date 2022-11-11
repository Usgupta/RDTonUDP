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
send_base = -1 #last ack pack
nextseqnum = 0 #latest unesent
rcvEOT = False
sentEOT = False
timeout = 0.1

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



# seqnums = []
# seqnums.append(nextseqnum)
# seqnums.append(3)
# print(seqnums)


# def sendEOT(emulator_addr, emulator_port, clientSocket, seqno):
#     data = ""
#     ptype = 2
#     seqno += 1
#     seqno=seqno%32
#     lendata = 0
#     packet = Packet(ptype,seqno,lendata,data)
#     clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

# MAXREADSIZE = 500
# emulator_addr = "129.97.167.46" #emulator address 014

# emulator_addr = "129.97.167.47" #emulator address 010
emulator_addr = "129.97.167.51" #emulator address 002
emulator_port = 39571 #emulator port
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

def timerout():
    # print(currno)
    # print(type(currno))
    global timer
    global windowsize
    global send_base
    global lock
    global timestamp
    print("GET TIMER LOCK")
    lock.acquire(timeout=1)
    
    print("TIMER out for......................",send_base+1)
    print("retransmitting.....")
    print("cancelling for and reset timer for no **********",send_base+1)
    timer.cancel()
    timer = threading.Timer(timeout,timerout)
    if not lastACK and packets[send_base+1]!=None:
        clientSocket.sendto(packets[send_base+1].encode(),(emulator_addr, emulator_port))
        windowsize = 1
        timestamp+=1
        addlog(seqnumlog,send_base+1)
        addlog(Nlog,windowsize)
        timer.start()
    lock.release()
    print("RELEASE TIMER LOCK")

    
timer = threading.Timer(timeout,timerout)

def makePackets():
    global pacseqno
    global sentEOT
    global timeout
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
                # sentEOT = True
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
            # sentEOT = True
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
    global timer
    while True:
        lock.acquire(timeout=1)

        if ((nextseqnum-send_base)<windowsize and packets[nextseqnum]!=None) or (send_base==-1 and nextseqnum==0):

            print("try acq lock send")
            print("Sending packet, ", nextseqnum)
            if (lastACK and (not sentEOT)):
                if packets[nextseqnum].typ==2: 
                    timestamp += 1

                    addlog(seqnumlog,"EOT") #add EOT to seq log
                    print("sending eot")
                    clientSocket.sendto(packets[nextseqnum].encode(),(emulator_addr, emulator_port))
                    sentEOT = True
                    timer.cancel()
                    # nextseqnum += 1
                    # nextseqnum= nextseqnum%32
                    print("release send lock")
                    lock.release()
            else:
                print(lastACK,sentEOT)
                if packets[nextseqnum].typ!=2:
                    timestamp += 1
                    # if nextseqnum==0:
                    #     print("starting timer for:",nextseqnum)
                        
                    clientSocket.sendto(packets[nextseqnum].encode(),(emulator_addr, emulator_port))
                    if nextseqnum==(send_base+1):
                        timer.cancel()
                        timer = threading.Timer(timeout,timerout)
                        timer.start()
                    addlog(seqnumlog,packets[nextseqnum].seqnum) #add seq num to seq log
                    nextseqnum += 1
                    nextseqnum= nextseqnum%32
                    print("release send lock")
                    lock.release()

                else:
        
                    print("its an eot but cant send rn")
                    print("release send lock")
                    lock.release()
                    time.sleep(0.01)
                    # time.sleep(10)
                    # lock.release()
            # print("release send lock")
            # lock.release()
            # lock.release()
            if rcvEOT:
            # print(nextseqnum,send_base)
                print("killing sending packets")
                # lock.release()
                sys.exit()
        else:
            if rcvEOT:
            # print(nextseqnum,send_base)
                print("killing sending packets")
                lock.release()
                sys.exit()
            lock.release()    
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
    global timer
    tempval = packets[0]
# threading.Timer(timeout, func,)
    while True:
        print("rec is scheduled")
        recvd_packet = Packet(clientSocket.recv(1024))
        # print(recvd_packet)
        # print(lock.locked())
        # if recvd_packet:
        print("try acq lock rec")
        # print(lock.locked())
        lock.acquire(timeout=1)
        timestamp+=1
        print("Received ack for .......", recvd_packet.seqnum)
        # print(recvd_packet)
        # print(lock.locked())
        if recvd_packet.typ == 2:
            print("got eot from rec")
            addlog(acklog,"EOT")
            send_base = recvd_packet.seqnum
            packets[:send_base+1]= [None] * len(packets[:send_base+1])
            # addlog(acklog,)
            clientSocket.close()
            rcvEOT = True
            timer.cancel()
            lock.release()
            sys.exit()
        else:
            print("its not eot")
            addlog(acklog,recvd_packet.seqnum) #add seq num to seq log
            if recvd_packet.seqnum > send_base:
                print("ack and rec until here: ", send_base)
                send_base = recvd_packet.seqnum
                print("cancelling and reset timer for no **********",send_base)
                timer.cancel()
                timer = threading.Timer(timeout,timerout)
                tempval = packets[send_base]
                packets[:send_base]= [None] * len(packets[:send_base])
                #restart timer here
                # send_base %= 32
                windowsize = min(windowsize+1,MAXN)
                addlog(Nlog,windowsize)
                makePackets()
                timer.start()
                if packets.count(None)==30 and pacseqno == None:
                    print("i hv got the last ack")
                    lastACK=True
                else:
                    print(packets.count(None))
                    # print(packets)
            if recvd_packet.seqnum == (send_base) and dupcount < 4:

                print("dup inc")
                dupcount += 1
            if dupcount == 4:
                print("retransmitting.....")
                print("cancelling for and reset timer for no **********",send_base)
                timer.cancel()
                timer = threading.Timer(timeout,timerout)
                clientSocket.sendto(tempval.encode(),(emulator_addr, emulator_port))
                timer.start()
                addlog(seqnumlog,send_base)
                windowsize = 1
                addlog(Nlog,windowsize)
                dupcount=0
            else:
                print("i got some ack which i didnt expect", recvd_packet.seqnum,send_base)
            print("release rec lock")
            lock.release()
        # else:
        #     print("didnt rec sleeping....")
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
