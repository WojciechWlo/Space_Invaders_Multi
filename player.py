import pygame
from bullet import Bullet_1

class PlayerSurface():
    __fields__ = 'window', 'x','y','w','h','id','n'
    def __init__(self, window,x,y,w,h, id):
        self.window = window
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.sprite=pygame.image.load("images/player"+str(id)+".png")
        self.sprite=pygame.transform.scale(self.sprite, (self.w,self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.id = id

    def draw(self):
        self.image.blit(self.sprite, (0,0))
        self.window.image.blit(self.image, self.rect)


class Player():
    def __init__(self, x,y,w,h,playerID ,screenWidth,screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.id = playerID
        self.speed = 6
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.i = 0
        self.iShot = 0
        self.iShotFreq = 10
        self.movement = dict()
        self.health = 20

    def update(self):
        self.move()

    def collision(self,obj):
        return self.x + self.w > obj.x and self.x < obj.x + obj.w and self.y + self.h > obj.y and self.y < obj.y + obj.h


    def shot(self, bullets):
        

        if self.iShot <self.iShotFreq:
            self.iShot+=1
        else:   
            if 'shot' in self.movement:
                self.iShot = 0
                bullets[self.id].append(Bullet_1(10, 10, self.x+self.w/2, self.y,0, 90, None))


    def move(self):
        if 'right' in self.movement:
            self.x +=self.speed
        if 'left' in self.movement:
            self.x -=self.speed
        if 'down' in self.movement:
            self.y +=self.speed
        if 'up' in self.movement:
            self.y -=self.speed

            

        
        if self.x <0:
            self.x = 0
        if self.x +self.w>self.screenWidth:
            self.x = self.screenWidth - self.w
        if self.y <0:
            self.y = 0
        if self.y+self.h> self.screenHeight:
            self.y = self.screenHeight - self.h
        
