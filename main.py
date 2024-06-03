#import subprocess, sys; subprocess.run([sys.executable, '-m', 'pip', 'install', 'https://inventwithpython.com/pygame/pygame-2.1.2-cp311-cp311-win_amd64.whl'])

import pygame
import sys
from player import PlayerSurface
from action_window import ActionWindow
import json
import argparse
from client import Client
from data_container import DataToSend
from data_container import DataContainer
from action import Action
from pygame._sdl2.video import Window
from enemy import EnemySurface
from bullet import BulletSurface

class Game(object):
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.window = Window.from_display_module()

        programIcon = pygame.image.load('images/player0.png')

        pygame.display.set_icon(programIcon)

        pygame.display.set_caption('Space Invaders')
        pygame.font.init()



        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.actionWindow = ActionWindow(520,560, self.screen)
        
        #self.all_players_sprites.add(Player(self.action_window.rect))
        self.running = True
        self.settings = self.load_settings('settings.json')

        for i in self.settings["player"]:
            self.nickname = i['nickname']

        ip = None
        port = None

        for i in self.settings["connection"]:
            ip = str(i['ip'])
            port = int(i['port'])

        self.client = Client(self.nickname, ip, port)
        
        initD= self.client.getInit()
        self.players = [None]*initD.n
        self.n = initD.n
        self.player = PlayerSurface(self.actionWindow,
                                    initD.x, 
                                    initD.y,
                                    initD.w, 
                                    initD.h,
                                    initD.id
                                    )

        self.players[self.player.id] = self.player


        self.enemies = []
        self.bullets = []

        self.nextStageFlag = False
        self.movement = dict()
        self.scores = [0]*self.n
        self.health = [0]*self.n
        self.status = [0]*self.n
        self.loop()


    def load_settings(self, file):
        f = open(file)
        data = json.load(f)
        f.close()
        return data


    def update_state(self):
        p = self.players[self.player.id]
        
        receivedD = self.client.send(p.id, self.movement)
        #print(receivedD.data)
        self.status = receivedD.status
        for i in range(len(receivedD.data)):
            if receivedD.status[i] == False:
                if self.players[receivedD.data[i].id] != None:
                    self.players[receivedD.data[i].id] = None
            else:
                if self.players[receivedD.data[i].id] ==None:
                    self.players[receivedD.data[i].id] = PlayerSurface(self.actionWindow,
                                                                        receivedD.data[i].x,
                                                                        receivedD.data[i].y,
                                                                        receivedD.data[i].w,
                                                                        receivedD.data[i].h,
                                                                        receivedD.data[i].id
                                                                        )                
                else:
                    self.players[receivedD.data[i].id].rect.x = receivedD.data[i].x
                    self.players[receivedD.data[i].id].rect.y = receivedD.data[i].y        
        self.nextStageFlag = receivedD.nextStageFlag
        self.bullets = []
        self.enemies= []
        for i, e in enumerate(receivedD.enemies):
            self.enemies.append(EnemySurface(self.actionWindow, e.x,e.y,e.w,e.h))

        for i in range(len(receivedD.bullets)):
            for j in range(len(receivedD.bullets[i])):
                b = receivedD.bullets[i][j]
                self.bullets.append(BulletSurface(self.actionWindow, i,b.x, b.y,b.w, b.h, self.n))

        for i in range(self.n):
            self.scores[i] = receivedD.score[i]
            self.health[i] = receivedD.health[i]
        #print(self.health[self.player.id])

    def loop(self): 

        while self.running:
            
            self.clock.tick(self.FPS)
            #print("kloc")
            self.movement = dict()

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit(0)

            keyState = pygame.key.get_pressed()
            if keyState[pygame.K_RIGHT]:
                self.movement['right'] = True
            if keyState[pygame.K_LEFT]:
                self.movement['left'] = True
            if keyState[pygame.K_DOWN]:
                self.movement['down'] = True
            if keyState[pygame.K_UP]:
                self.movement['up'] = True
            if keyState[pygame.K_e]:
                self.movement['shot'] = True
            self.update_state()
            self.update()
            self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i in range(int(self.height/20)):
            pygame.draw.rect(self.screen, (10,10,10), pygame.Rect(0,i*20, self.width, 1))
        for j in range(int(self.width/20)):
            pygame.draw.rect(self.screen, (10,10,10), pygame.Rect(j*20,0, 1, self.height))

        self.actionWindow.draw()
        for p in self.players:
            if p != None:
                p.draw()


        for e in self.enemies:
            e.draw()

        for b in self.bullets:
            b.draw()
            
        font = pygame.font.SysFont('Comic Sans MS', 15)
        for i in range(self.n):

            color = (0,0,0)
            if self.status[i]!=True:
                color = (50,50,50)
            elif i ==0:
                color = (255,0,0)
            elif i == 1:
                color = (0,255,0)
            elif i == 2:
                color = (0,0,255)
            elif i == 3:
                color = (255,255,0)
            textSurface = font.render('Player '+str(i+1), False, color)
            #text_surface = self.my_font.render('Some Text', False, (255, 0, 0))
            self.screen.blit(textSurface, (570,20+i*90))
            textSurface = font.render('health: '+str(self.health[i]), False, color)
            self.screen.blit(textSurface, (570,40+i*90))
            textSurface = font.render('score: '+str(self.scores[i]), False, color)
            self.screen.blit(textSurface, (570,60+i*90))
        #    p.draw()
       
        #for p in self.players:
        #    p.draw()

        #self.players.draw(self.screen)

        pygame.display.flip()
    
    def update(self):
        self.actionWindow.update()
        #self.action.update_frame(self.syncFrame)
        #self.player.update()
        '''
        for e in self.enemies:
            e.update()
        '''

if __name__ == "__main__":
    Game()