import pygame

class ActionWindow():
    def __init__(self, width, height, screen):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.sprites = []
        self.sprites.append(pygame.image.load("images/actionBackground.png"))
        self.sprites.append(pygame.image.load("images/actionBackground.png"))
        self.spritesY = [0,height]
        #self.color = (0,0,60)
        #self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.screen = screen

    def update(self):
        for i in range(len(self.sprites)):
            self.spritesY[i]+=3
            if self.spritesY[i]>self.image.get_height():
                self.spritesY[i] -= self.image.get_height()*len(self.sprites)

    def draw(self):
        self.screen.blit(self.image, (20,20))
        for i in range(len(self.sprites)):
            self.image.blit(self.sprites[i],(0,self.spritesY[i]))
            #self.image.blit(sprite,(0,0))