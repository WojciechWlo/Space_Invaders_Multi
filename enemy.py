import pygame
import math
from bullet import Bullet_2

class EnemySurface():
    __fields__ = 'window', 'x','y','w','h','id'
    def __init__(self, window, x,y,w,h):
        self.window = window
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.sprite = pygame.image.load("images/enemy0.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.w,self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image.blit(self.sprite, (0,0))
        self.window.image.blit(self.image, self.rect)


class Enemy():
    def __init__(self, w,h, name,index, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.index = index
        self.color = (255,255,255)
        self.w = w
        self.h = h
        self.i = 0
        self.health =0
        self.sX = 0
        self.sY = 0
        self.speed = 0
        self.r = 0
        self.alpha = 0
        self.name = name
        self.x = 0
        self.y = 0
        self.i = 0
        self.iShot = 0
        self.iShotFreq = 0
        self.score = 10


    def collision(self,obj):
        return self.x + self.w > obj.x and self.x < obj.x + obj.w and self.y + self.h > obj.y and self.y < obj.y + obj.h


    def update(self):
        pass
    
    def calculate_position(self):
        self.x = self.sX + self.r*math.cos(self.alpha*math.pi/180)
        self.y = self.sY + self.r*math.sin(self.alpha*math.pi/180)


class Enemy_1(Enemy):
    def __init__(self, w, h, sX, sY,r, alpha, index, screenWidth, screenHeight):
        super().__init__(w,h,self.__class__.__name__, index, screenWidth, screenHeight)
        self.sX = sX
        self.sY = sY
        self.r = r
        self.alpha = alpha
        self.speed =3
        self.direction = False
        self.iShotFreq = 60
        self.health = 10
        self.calculate_position()

    
    def shot(self,bullets):
        if self.iShot <self.iShotFreq:
            self.iShot+=1
        else:   
            self.iShot= 0
            bullets[len(bullets)-1].append(Bullet_2(10, 10, self.x+self.w/2, self.y,0, 90, None))
    

    def update(self):
        self.i += 1
        if self.i < 150:
            self.sX +=self.speed
        else:
            self.alpha +=self.speed                
        self.calculate_position()
