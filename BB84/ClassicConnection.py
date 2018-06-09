import socket

alicePort = 1234
evePort = 1235
bobPort = 1236

def createLocalhostServerSocket(port):
    # create an INET, STREAMing socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serverSocket.bind(("localhost", port))
    # become a server socket
    serverSocket.listen(5)
    return serverSocket

def receiveInt(serverSocket):
    (clientSocket, address) = serverSocket.accept()
    # receive one byte
    byte = clientSocket.recv(1)
    return int.from_bytes(byte, byteorder="little")

def receive2Ints(serverSocket):
    (clientSocket, address) = serverSocket.accept()
    # receive two bytes
    bytes = clientSocket.recv(2)
    return (bytes[0], bytes[1])

def createSocket():
    # create an INET, STREAMing socket
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendIntToLocalhost(integer, port):
    clientSocket = createSocket()
    # now connect to the web server on port 80 - the normal http port
    clientSocket.connect(("localhost", port))
    clientSocket.send(integer.to_bytes(1, "little"))
    clientSocket.close()

def send2IntsToLocalhost(integerOne, integerTwo, port, clientSocket):
    clientSocket = createSocket()
    # now connect to the web server on port 80 - the normal http port
    clientSocket.connect(("localhost", port))
    clientSocket.send(bytes([integerOne, integerTwo]))
    clientSocket.close()

def closeSocket(socket):
    socket.close()
