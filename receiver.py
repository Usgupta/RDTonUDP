# import imp
import pathlib
from socket import *
import sys
import time
from datetime import datetime
import secrets
import traceback



def convert_int_to_bytes(x):
    """
    Convenience function to convert Python integers to a length-8 byte representation
    """
    return x.to_bytes(8, "big")


def convert_bytes_to_int(xbytes):
    """
    Convenience function to convert byte value to integer value
    """
    return int.from_bytes(xbytes, "big")


def read_bytes(socket, length):
    """
    Reads the specified length of bytes from the given socket and returns a bytestring
    """
    buffer = []
    bytes_received = 0
    while bytes_received < length:
        data = socket.recv(min(length - bytes_received, 1024))
        if not data:
            raise Exception("Socket connection broken")
        buffer.append(data)
        bytes_received += len(data)

    return b"".join(buffer)


def main(args):
    # port = int(args[0]) if len(args) > 0 else 4321
    # address = args[1] if len(args) > 1 else "localhost"

    

    try:

        emulator_addr = "129.97.167.27" #emulator address
        emulator_port = 15539 #emulator port
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        rec_port = 9994
        # serverPort = port
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', rec_port)) 
                            # If the packet is for transferring a chunk of the file
                            # start_time = time.time()

                            # file_len = convert_bytes_to_int(
                                # read_bytes(client_socket, 8)
                            # )
                            # file_data = read_bytes(client_socket, file_len)
                            # print(file_data)

        filename = "rec.txt"

        recvd_packet = serverSocket.recv(1024)
        print("got the packet")

        typ, seqnum, length, data = recvd_packet.decode()
        print("packet vals are", typ,seqnum,length,data)
        if typ==2:
            print("EOT")
            exit()
        else:



        # message1, clientAddress = serverSocket.recvfrom(2048) 
        # message2, clientAddress = serverSocket.recvfrom(2048) 


        # Write the file with 'recv_' prefix
            with open(
                filename, mode="wb"
            ) as fp:

                fp.write(data)

                # fp.write(message2)
            print("finidhed"
                # f"Finished receiving file in {(time.time() - start_time)}s!"
            )
    except Exception as e:
        print(e)
        # s.close()


if __name__ == "__main__":
    main(sys.argv[1:])