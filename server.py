import socket
import threading
import argparse
import pickle
from data_container import DataContainer
from data_container import DataToSend
from data_container import InitData
import pygame
from action import Action
from player import Player
import struct

class Server(object):
    def __init__(self, n = 2, address = "127.0.0.1", port = 12345):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s = None
        self.server_address = address
        self.port = port
        self.format = "utf-8"
        self.n = n
        self.Bytes = 2048
        self.windowHeight = 560
        self.windowWidth = 520
        try:
            self.s.bind((self.server_address, self.port))
            #self.s = Listener((self.server_address,self.port))
        except socket.error as e:
            str(e)

        self.s.listen(self.n)

        self.players = [Player(self.windowWidth*0.5-25,self.windowHeight*0.75,30,30,0,self.windowWidth,self.windowHeight),
                        Player(self.windowWidth*0.5-25,self.windowHeight*0.75,30,30,1,self.windowWidth,self.windowHeight),
                        Player(self.windowWidth*0.5-25,self.windowHeight*0.75,30,30,2,self.windowWidth,self.windowHeight),
                        Player(self.windowWidth*0.5-25,self.windowHeight*0.75,30,30,3,self.windowWidth,self.windowHeight)
                        ]

        self.currentPlayer = 0
        
        self.connectedPlayers = [None]*n
        self.nextStageImpulse = [False]*n
        self.frame = [0]*n
        self.working = False
        self.currentStage = 0
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.actionFlag = False
        self.action = Action(self.windowWidth,self.windowHeight)
        self.enemies = []

        self.bullets = []
        for i in range(n+1):
            self.bullets.append([])

        self.scores = [0]*n
        self.start_communication()


    
        


    def prepare_next_stage(self, player):
        flag = False
        if self.nextStageImpulse[player] == False:
            if self.currentStage==0:
                if sum(x is None for x in self.connectedPlayers)==0:
                    self.frame = [0]*self.n
                    self.nextStageImpulse[player] = True
                    self.actionFlag = True
                    flag = True
            else:
                pass

        if sum(x is True for x in self.nextStageImpulse)==self.n:
            self.currentStage +=1
            self.nextStageImpulse = [False]*self.n

        return flag

    def add_client(self):

        l = len(self.connectedPlayers)
        
        for i in range(l):
            if self.connectedPlayers[i] == None:
                self.connectedPlayers[i] = i
                return i




    def update_bullets(self):
        for i in range(len(self.bullets)):
            j = 0
            while j <len(self.bullets[i]):
                self.bullets[i][j].update()
                if i <self.n:
                    if self.bullets[i][j].y+self.bullets[i][j].h<0:
                        self.bullets[i].pop(j)
                        j-=1
                else:
                    if self.bullets[i][j].y>self.windowHeight:
                        self.bullets[i].pop(j)                    
                        j-=1
                j+=1

    def main_loop(self):
        while True:
            if self.actionFlag == True:
                self.action.check_enemies_health(self.enemies, self.bullets, self.scores)
                self.action.check_players_health(self.bullets, self.players)
                self.action.update(self.enemies,self.bullets)


            self.update_bullets()
            
            for p in self.players:
                p.update()
                p.shot(self.bullets)

            self.clock.tick(self.FPS)

        


    def threaded_client(self, connection):
        
        player = self.add_client()

        connection.send((pickle.dumps(InitData(self.players[player].x,
                                               self.players[player].y,
                                               self.players[player].w,
                                               self.players[player].h,
                                               self.n,
                                               player))))


        reply = ""
        while True:
            try:
                data = connection.recv(self.Bytes)


                if not data:
                    print("Disconnected")
                    self.connectedPlayers[player] = None
                    break
                else:
                    data = pickle.loads(data)
                    self.players[player].movement = data.movement

                    reply = DataContainer(self.n)
                    for i in range(self.n):
                        
                        reply.data[i] = DataToSend(self.players[i].x,
                                                    self.players[i].y,
                                                    self.players[i].w,
                                                    self.players[i].h,
                                                    None,
                                                    self.players[i].id,
                                                    )
                        #print(reply.data[i].index)
                        if self.connectedPlayers[i] == None:
                            reply.status[i] = False
                        else:
                            reply.status[i] = True


                    #print(self.frame)

                    #reply.enemiesOperation = self.action.operation
                    for i, e in enumerate(self.enemies):
                        reply.enemies.append(DataToSend(e.x,e.y,e.w,e.h,None,e.index))

                    #print(len(self.bullets),len(self.bullets[i]))
                    #print(self.bullets)
                    for i in range(len(self.bullets)):
                        for j in range(len(self.bullets[i])):
                            b= self.bullets[i][j]
                            reply.bullets[i].append(DataToSend(b.x,b.y,b.w,b.h,None,b.index))
                            
                    for i in range(self.n):
                        reply.score[i] = self.scores[i]
                        reply.health[i] = self.players[i].health

                reply.nextStageFlag = self.prepare_next_stage(player)
                
                #print(len(pickle.dumps(reply)))
                connection.send(pickle.dumps(reply))
                #-------------------------------------------------
                '''
                packet = pickle.dumps(reply)
                length = struct.pack('!I', len(packet))
                packet = length +packet
                connection.sendall(packet)
                '''
                

            except socket.error as e:
                self.connectedPlayers[player] = None
                #print(e)
                break


    def start_communication(self):
        mainLoop = threading.Thread(target=self.main_loop, args=())
        mainLoop.start()
        while True:
            print("Waiting for clients: ")
            connection, client_address = self.s.accept()
            print("Client just joined server: ",self.server_address)
            r_t  = threading.Thread(target=self.threaded_client, args=(connection,))
            r_t.start()


ap = argparse.ArgumentParser()
ap.add_argument("-n", "--clients", type=int, default=2, help="Allowed clients number")
ap.add_argument("-a", "--address", type=str, default="127.0.0.1", help="Host IP adress")
ap.add_argument("-p", "--port", type=int, default=12345, help="Host port")
args = vars(ap.parse_args())
server = Server(n=args["clients"], address = args["address"], port = args["port"])
