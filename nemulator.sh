#!/bin/bash

#For Python implementation
python3 network_emulator.py 60482 "129.97.167.52" 28850 62032 "129.97.167.27" 29785 0 0 1
# python3 network_emulator.py <Forward receiving port> <Receiver's network address> <Reciever’s receiving UDP port number> <Backward receiving port> <Sender's network address> <Sender's receiving UDP port number> <Maximum Delay> <drop probability> <verbose>
