#!/bin/bash

#Run script for the server distributed as a part of 
#Assignment 1
#Computer Networks (CS 456 / CS 656)
#
#Number of parameters: 1
#Parameter:
#    $1: <req_code>
#

#Uncomment exactly one of the following commands depending on implementation

#For C/C++ implementation
#./server $1

#For Java implementation
#java server $1 

#For Python implementation
python3 network_emulator.py 39571 "129.97.167.51" 52081 1037 "129.97.167.27" 2658 1 0 1

#For Ruby implementation
#ruby server.rb $1
