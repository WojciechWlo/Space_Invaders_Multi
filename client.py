import threading
import socket
import argparse
import pickle
from data_container import ClientData
import struct

class Client(object):
    def __init__(self, nickname, server_address, port):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #self.s = None
        
        self.server_address = server_address
        self.port = port
        self.format = "utf-8"
        self.nickname = nickname
        self.Bytes = 4096*1024
        self.initData = self.connect()

    def getInit(self):
        return self.initData

    def connect(self):
        try:
            
            self.s.connect((self.server_address, self.port))
            
            #self.s = Cl((self.server_address,self.port))
            
            return pickle.loads(self.s.recv(self.Bytes))
        

            #return pickle.loads(self.s.recv())
        except socket.error as e:
            print(e)


    def send(self,id, movement):
        while True:
            try:
                data = ClientData( id)
                data.movement = movement
                self.s.send(pickle.dumps(data))

                return pickle.loads(self.s.recv(self.Bytes))
            
            
            
            except socket.error as e:
                print(e)

    def communication(self):
        s_t = threading.Thread(target=self.send)
        s_t.start()
        r_t = threading.Thread(target=self.receive)
        r_t.start()
