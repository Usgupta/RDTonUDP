from socket import *
from random import *
import sys
import pathlib

from packet import Packet


from socket import *

seqnumlog = "seqnum.log"
acklog = "ack.log"
Nlog = "N.log"

timestamp = 0

windowsize = 1
MAXN = 10
send_base = 0
nextseqnum = 0


alllogfiles = [seqnumlog,acklog,Nlog]
for i in range(3):
    file = open(alllogfiles[i],"w")
    file.close()

def addlog(file_name,data):
    with open(file_name, mode="a") as fp:
        print("opened {file_name} file")
        fp.write(str(timestamp) + " " + str(data) + "\n")

def sendEOT(emulator_addr, emulator_port, clientSocket, seqno):
    data = ""
    ptype = 2
    seqno += 1
    seqno=seqno%32
    lendata = 0
    packet = Packet(ptype,seqno,lendata,data)
    clientSocket.sendto(packet.encode(),(emulator_addr, emulator_port))

MAXREADSIZE = 500
# emulator_addr = "129.97.167.46" #emulator address 014

# emulator_addr = "129.97.167.47" #emulator address 010
emulator_addr = "129.97.167.51" #emulator address 002
emulator_port = 14836 #emulator port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sender_port = 2658
clientSocket.bind(('', sender_port)) 

# print(sender_port)


# integer type; # // 0: ACK, 1: Data, 2: EOT
# integer seqnum; # // Modulo 32
# integer length; # // Length of the String variable ‘data’ // String with Max Length 500
# String data;

filename = "longtest.txt"

while filename != "-1" and (not pathlib.Path(filename).is_file()):
    filename = input("Invalid filename. Please try again:").strip()

# if filename == "-1":
#     s.sendall(convert_int_to_bytes(2))
#     break

# filename_bytes = bytes(filename, encoding="utf8")

# Send the filename
# clientSocket.sendto(filename.encode(),(serverName, serverPort))
# s.sendall(convert_int_to_bytes(0))
# s.sendall(convert_int_to_bytes(len(filename_bytes)))
# clientSocket.sendto(filename_bytes,(emulator_addr, emulator_port))
with open(filename, mode="r") as fp:
    data = fp.read()
# Send the file
readptr = 0
packets = [None] * 32

def makePackets():
    if len(data)>500:
        while(readptr<=len(data)):
            if(len(packets)==32 and packets.count(None) == 0):
                break
            seqno = packet.index(None)
            ptype = 1
            lendata = len(data[readptr:min(i+500,len(data))])
            print(readptr)
            print(data[i:min(readptr+500,len(data))])
            packet = Packet(ptype,seqno,lendata,data[readptr:min(readptr+500,len(data))])
            packets[seqno] = packet
            readptr+=500
    else:
        packets[0] = packet(1,0,len(data),data)

    if readptr>len(data) or len(data)<500:
        seqno = packet.index(None)
        ptype = 2
        lendata = 0
        packets[seqno] = Packet(ptype,seqno,lendata,"")

def sendPackets(packets):
    if nextseqnum-send_base!=windowsize:
        clientSocket.sendto(packets[nextseqnum].encode(),(emulator_addr, emulator_port))
        timestamp+=1
        addlog(seqnumlog,packets[nextseqnum].seqnum) #add seq num to seq log
        nextseqnum+=1
        nextseqnum=nextseqnum%32
    # if dup:
        
filepackets = makePackets(filename)
dupcount = 0
def recAck(packets):
    recvd_packet = Packet(clientSocket.recv(1024))
    timestamp+=1
    print(recvd_packet)
    addlog(acklog,recvd_packet.seqnum) #add seq num to seq log

    if recvd_packet.seqnum == send_base:
        packets[:send_base+1]=None
        send_base+=1
        send_base%=32
        windowsize = min(windowsize+1,MAXN)
    elif recvd_packet.seqnum == send_base-1 and dupcount<3:
        dupcount+=1
    elif dupcount==3:
        clientSocket.sendto(packets[send_base].encode(),(emulator_addr, emulator_port))
        windowsize = 1
        dupcount=0
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

sendEOT(emulator_addr, emulator_port, clientSocket, seqno)
print("rec pack")
recvd_packet = clientSocket.recv(1024)
print(recvd_packet)
typ, seqnum, length, data = Packet(recvd_packet).decode()
if typ==2:
    print("got eot from rec")
    clientSocket.close()