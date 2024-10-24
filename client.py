import socket
from threading import Thread
import os
import time
import json
import psutil

class Client:

    def __init__(self, host, port, interval):
        self.interval = interval
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.name = input("Enter the name:")
        self.talkToServer()
    
    def talkToServer(self):
        self.socket.send(b"{self.name}")
        Thread(target=self.receiveMessage).start()
        Thread(target=self.sendMessage).start()
    
    def sendMessage(self):
        while True:
            clientMessage = {"name": self.name, "time":str(time.time()), "cpu": str(psutil.cpu_percent()), "ram": str(psutil.swap_memory().percent), "disk":str(psutil.disk_usage("C:\\").percent)}
            self.socket.send(json.dumps(clientMessage).encode("utf-8"))
            time.sleep(self.interval)
    
    def receiveMessage(self):
        while True:
            serverMessage = self.socket.recv(1024).decode('utf-8')
            print(serverMessage)

if __name__ == "__main__":
    Client("192.168.1.128", 9876, 30)