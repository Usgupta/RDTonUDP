# RDTonUDP
implement a congestion controlled pipelined Reliable Data Transfer (RDT) protocol over UDP, which could be used to transfer a text file from one host to another across an unreliable network. 

UMANG GUPTA 20877808

## How to run your program

#### NOTE: RUN ALL 3 FILES ON DIFFERENT SERVERS AND MAKE SURE THE IP ADDRESSESS ARE PROVIDED CORRECTLY FOR EACH

### Running the Network Emulator

Run the following command in terminal to run the network emulator `./nemulator.sh`

To change the arguements of network emulator edit the `./nemulator.sh` file

Use the order present in the comments for order

### Running the Sender

Run the following command in terminal to run the network emulator `./sender.sh`

To change the arguements of network emulator edit the `./sender.sh` file

Use the order present in the comments for order

### Runnning the Receiver

Run the following command in terminal to run the network emulator `./receiver.sh`

To change the arguements of network emulator edit the `./receiver.sh` file

Use the order present in the comments for order

## Undergrad machines your program was built and tested on

The program was built on Mac Intel 2020 running OS 12.5.1

It has been tested on the following, running client and server on same machine as well as running them on different machines
• ubuntu2004-002.student.cs.uwaterloo.ca
• ubuntu2004-004.student.cs.uwaterloo.ca
• ubuntu2004-008.student.cs.uwaterloo.ca
• ubuntu2004-010.student.cs.uwaterloo.ca
• ubuntu2004-014.student.cs.uwaterloo.ca

### Version of make used

Make is not used for this program as it is written completely in python

### Version of compiler used

Built on python3 version 3.10.5

Tested successfully using python3 version 3.8.10 on ubuntu2004-008,ubuntu2004-004,ubuntu2004-002,ubuntu2004-014,ubuntu2004-010