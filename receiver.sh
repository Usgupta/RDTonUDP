#!/bin/bash

#For Python implementation
 
python3 receiver.py "129.97.167.47" 62032 28850 receive.txt
# python3 <hostname for the network emulator>, <UDP port number used by the link emulator to receive ACKs from the receiver>, <UDP port number used by the receiver to receive data from the emulator>, and <name of the file into which the received data is written> in the given order.