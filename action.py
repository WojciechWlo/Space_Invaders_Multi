import pygame
from enemy import Enemy_1

class Action():
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.stage = 0
        self.start = False
        self.i = 0
        self.operation = ""
        self.ready = False

    def next_stage(self,enemies):
        self.stage += 1
        self.i = 0
        enemies = []


    def prepare_stage(self, enemies):
        
        if self.stage == 1:
            if self.i >0 and self.i<2:
                self.ready = False
                self.operation = "create"
                for i in range(5):
                    enemies.append(Enemy_1(30,30,-50-i*60,100, 20,90, None,self.screenWidth,self.screenHeight))
                self.ready = True
                self.operation = "update"
            elif self.i >200 and self.i <202:
                self.ready = False
                self.operation = "create"
                for i in range(5):
                    enemies.append(Enemy_1(30,30,-50-i*60,200, 20,90, None,self.screenWidth,self.screenHeight))
                self.ready = True
                self.operation = "update"                

    def check_players_health(self, bullets,players):
        b = 0
        while b < len(bullets[len(bullets)-1]):
            attackedPlayers = [None]*len(players)
            p = 0
            while p < len(players):
                if players[p].collision(bullets[len(bullets)-1][b]):
                    attackedPlayers[p] = True
                p+=1
            if True in attackedPlayers:
                damage = int(bullets[len(bullets)-1][b].damage/attackedPlayers.count(True))
                if damage <1:
                    damage = 1
                bullets[len(bullets)-1].pop(b)
                for p in range(len( players)):
                    if attackedPlayers[p] == True:
                        players[p].health -=damage
                b-=1
            b+=1

    def check_enemies_health(self,enemies, bullets, playerScores):
        
        e = 0
        while e <len(enemies):
            i=0
            assistKill = [None]*(len(playerScores))
            while i < len(bullets)-1:
                j = 0
                '''
                print(i, len(bullets)-1)
                print(e, len(enemies))
                print(j, len(bullets[i]))
                print(bullets)
                '''
                while j < len(bullets[i]):

                    if enemies[e].collision(bullets[i][j]):
                        

                        bullets[i].pop(j)
                        j-=1
                        enemies[e].health -=1
                        if enemies[e].health<=0:
                            assistKill[i] = True
                            j = len(bullets[i])
                    j+=1
                i+=1
            if enemies[e].health<=0:

                score = enemies[e].score
                score = int(score/assistKill.count(True))
                for a in range(len(assistKill)):
                    if assistKill[a] == True:
                        playerScores[a]+=score
                enemies.pop(e)
                e-=1
            e+=1

    def check_stage(self,enemies):
        if self.stage == 0:
            self.next_stage(enemies)
        elif self.stage == 1:
            pass

    def update(self, enemies,bullets):
        self.check_stage(enemies)
        self.i += 1
        self.prepare_stage(enemies)

        self.ready = False
        for e in enemies:
            e.update()
            e.shot(bullets)
        self.ready = True

        