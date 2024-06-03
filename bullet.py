import pygame
import math

class BulletSurface():
    __fields__ = 'window', 'x','y','w','h'
    def __init__(self, window,id, x,y,w,h,n):

        self.w = w
        self.h = h
        self.sprite = None
        if id==n:
            self.sprite=pygame.image.load("images/ebullet0.png")
        else:
            self.sprite=pygame.image.load("images/pbullet"+str(id)+".png")       
        self.sprite=pygame.transform.scale(self.sprite, (self.w,self.h))
        self.window = window
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):
        self.image.blit(self.sprite, (0,0))
        self.window.image.blit(self.image, self.rect)


class Bullet():
    def __init__(self, w,h, name,index):
        self.index = index
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
        self.damage = 1

    def update(self):
        pass
    
    def calculate_position(self):
        self.x = self.sX + self.r*math.cos(self.alpha*math.pi/180)
        self.y = self.sY + self.r*math.sin(self.alpha*math.pi/180)

class Bullet_1(Bullet):
    def __init__(self, w, h, sX, sY,r, alpha, index):
        super().__init__(w,h,self.__class__.__name__, index)
        self.sX = sX -self.w/2
        self.sY = sY -self.h/2
        self.r = r
        self.alpha = alpha
        self.speed =10
        self.calculate_position()

    def move(self):
        self.sY -=self.speed
        self.calculate_position()
    
    def update(self):
        self.move()

class Bullet_2(Bullet):
    def __init__(self, w, h, sX, sY,r, alpha, index):
        super().__init__(w,h,self.__class__.__name__, index)
        self.sX = sX -self.w/2
        self.sY = sY
        self.r = r
        self.alpha = alpha
        self.speed =6
        self.calculate_position()

    def move(self):
        self.sY +=self.speed
        self.calculate_position()
    
    def update(self):
        self.move()