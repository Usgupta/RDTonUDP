#!/bin/bash

#For Python implementation
 
python3 sender.py "129.97.167.47" 60482 29785 0.1 longtest.txt
# python3 <host address of the network emulator>, <UDP port number used by the emulator to receive data from the sender>, <UDP port number used by the sender to receive ACKs from the emulator>, <timeout interval in units of millisecond>, and <name of the file to be transferred>