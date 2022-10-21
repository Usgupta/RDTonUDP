from socket import *
import sys

serverPort = 12000


serverSocket = socket(AF_INET,SOCK_STREAM)
try: 
    serverSocket.bind(('',serverPort))
except OSError:
    #if the default port is occupied it will choose a random available port 
    print("Default port 12000 was occupied, using a different port to run the server")
    newsock = socket()
    newsock.bind(('', 0)) 
    serverPort = newsock.getsockname()[1]

print("SERVER_PORT=",serverPort)


while True:
    serverSocket.listen(1)
    print('The server is ready to receive')

    # get the request code and convert it into integer
    try: 
        req_code = int(sys.argv[1])
    # if the request code is not an integer print the error and exit from the program
    except ValueError:
        print("req code must be an integer, exiting the server program")
        sys.exit()
    # if the request code was not entered then print the error and exit from the program
    except IndexError:
        print("please enter a req code, exiting the server program")
        sys.exit()

    print("req code of server is ", req_code)

    #accept connections from client for negotiations on TCP
    TCP_connectionSocket, addr = serverSocket.accept()
    rec_req_code = TCP_connectionSocket.recv(1024).decode() 

    #checking whether req code is valid
    if req_code == int(rec_req_code):
        print("request code has been verified successfully, generating random port for UDP connection...")

        randsock = socket()
        # the OS will pick a port for us and assign to the new socket created
        randsock.bind(('', 0)) 
        r_port = randsock.getsockname()[1]
        # send the random port generated to the client 
        TCP_connectionSocket.send(str(r_port).encode())

        #create udp socket using randomly generated port r_port

        UDP_serverSocket = socket(AF_INET, SOCK_DGRAM)
        UDP_serverSocket.bind(('', r_port)) 
        print("The UDP server is ready to receive")
        # udp client server file transfer on random port until the client sends a exit message
        while True:
            message, clientAddress = UDP_serverSocket.recvfrom(2048) 
            if message.decode() == 'EXIT':
                print("exiting tcp connection with client on port: ", r_port)
                break

            modifiedMessage = message.decode()[::-1]
            UDP_serverSocket.sendto(modifiedMessage.encode(),
        clientAddress)      


    else:
        #close the negotiation TCP connection if the request code was entered wrong
        print("req code mismatch, server req code is: ", req_code, " received req code is: ", rec_req_code, " closing the TCP connection")
        TCP_connectionSocket.close()
