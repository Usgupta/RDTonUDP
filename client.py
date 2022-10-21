from socket import *
from random import *
import sys

# #the default value of server address is that of a localhost so it assumes that the server and client are on the same machine
server_addr = "127.0.0.1"
# n_port = 12000

try: 
    server_addr = sys.argv[1]
#checks if no arguement was passed as the server address
except IndexError:
    print("Please enter a server address, exiting the client program")
    sys.exit()

try: 
    n_port = int(sys.argv[2])
#checks if no arguement was passed as for port number
except IndexError:
    print("Please enter a port number, exiting the client program")
    sys.exit()
#if the port entered is not an integer print the error and exit 
except ValueError:
    print("invalid port number passed, exiting the client program")
    sys.exit()

try: 
    req_code = int(sys.argv[3])
#checks if no arguement was passed as for request code 
except IndexError:
    print("Please enter a request code to negotiate with server, exiting the client program")
    sys.exit()
#if the request code entered is not an integer print the error and exit 
except ValueError:
    print("req code must be an integer, exiting the client program")
    sys.exit()

inputs = []

#gets the strings and stores them in a list
def getstr(inputs):
    i = 4
    try:
        while (sys.argv[i]):
            inputs.append(sys.argv[i])
            i+=1
    #if there is index error means there are no more strings being passed
    except IndexError:
        return
    

getstr(inputs)

print("Trying to connect to server address:  ",server_addr, " at port: ",n_port)

clientSocket = socket(AF_INET, SOCK_STREAM)

try: 
    clientSocket.connect((server_addr,n_port)) 
except ConnectionRefusedError:
    print("invalid socket address or the given port is not accepting connections")
    sys.exit()

#send the request code to the server to negotiate

clientSocket.send(str(req_code).encode()) 

r_port = clientSocket.recv(1024) 

try:
    r_port = int(r_port.decode())
    
except ValueError:
    print("invalid random port received might be due to wrong request code, exiting the program")
    sys.exit()

print("Negotiation successful, port for udp connection is: ", r_port)

clientSocket.close()


try: 
    clientSocket = socket(AF_INET, SOCK_DGRAM)
except:
    print("Client couldnt create a UDP socket exiting the client program, run the client to try again")
    sys.exit()

#send each string to the server until there is no message left in the list of strings
for i in range(len(inputs)):
    message = inputs[i]
    clientSocket.sendto(message.encode(),(server_addr, r_port)) 
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print("reversed string of,",message," is: ")
    print(modifiedMessage.decode())

#send exit message to exit the udp connection as all strings have been processed
message = 'EXIT'
print("exiting UDP connection and client program")
clientSocket.sendto(message.encode(),(server_addr, r_port))