#coding=utf-8
import socket
from multiprocessing import Process
import re


def handleClient(clientSocket):
    recvData = clientSocket.recv(1024)
    requestHeaderLines = recvData.splitlines()
    for line in requestHeaderLines:
        print(line)

    httpRequestMethodLine = requestHeaderLines[0]
    getFileName = re.match("[^/]+(/[^ ]*)", httpRequestMethodLine).group(1)
    print("file name is ===>%s"%getFileName) #for test

    if getFileName == '/':
        getFileName = documentRoot + "/index.html"
    else:
        getFileName = documentRoot + getFileName

    print("file name is ===2>%s"%getFileName) #for test

    try:
        f = open(getFileName)
    except IOError:
        responseHeaderLines = "HTTP/1.1 404 not found\r\n"
        responseHeaderLines += "\r\n"
        responseBody = "====sorry ,file not found===="
    else:
        responseHeaderLines = "HTTP/1.1 200 OK\r\n"
        responseHeaderLines += "\r\n"
        responseBody = f.read()
        f.close()
    finally:
        response = responseHeaderLines + responseBody
        clientSocket.send(response)
        clientSocket.close()


def main():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("",4444))
    serverSocket.listen(10)
    while True:
        clientSocket,clientAddr = serverSocket.accept()
        clientP = Process(target = handleClient, args = (clientSocket,))
        clientP.start()
        clientSocket.close()



documentRoot = './html'

if __name__ == '__main__':
    main()