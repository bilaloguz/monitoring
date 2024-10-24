import socket
from threading import Thread
from tinydb import TinyDB, Query
import time
import json

class Server:

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        print("Server waiting for new connection...")
        self.clientDB = TinyDB("dbs/client.db")
        self.messageDB = TinyDB("dbs/message.db" )

    def listen(self):
        while True:
            clientSocket, clientAddress = self.socket.accept()
            print("Connection from {clientAddress}", clientAddress)
            clientName = clientSocket.recv(1024).decode("utf-8")
            client = {"clientName": clientName, "clientSocket": clientSocket, "clientAddress": clientAddress}
            Thread(target=self.handleNewClient, args=(client, )).start()
    
    def handleNewClient(self, client):
        clientSocket = client['clientSocket']
        while True:
            clientMessage = clientSocket.recv(1024).decode('utf-8')
            #self.clientDB.insert({"clientName":client['clientName'], "clientSocket": clientSocket, "clientAddress": client["clientAddress"], "time": time.time(), "status": "online"})
            self.messageDB.insert(json.loads(clientMessage))

    def sendMessage(self, clientName, message):
        clientQuery = Query()
        client = self.clientDB.search((clientQuery.clientName == clientName) & (clientQuery.status == "online"))
        if client:
            client.clientSocket.send(message.encode("utf-8"))

if __name__ == "__main__":
    server = Server("192.168.1.128", 9876)
    server.listen()