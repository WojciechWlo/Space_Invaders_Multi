

class ClientData():
    def __init__(self, id):
        self.id = id
        movement = dict()

class DataToSend():
    def __init__(self,x,y,w,h,color, id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.id = id

class InitData():
    def __init__(self, x,y,w,h,n,id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.n = n
        self.id = id

class DataContainer():
    def __init__(self,n):
        self.data = [None]*n
        self.status = [None]*n
        self.score = [None]*n
        self.nextStageFlag = False
        self.enemies = []
        self.bullets = []
        self.health = [0]*n
        for i in range(n+1):
            self.bullets.append([])
        self.enemiesOperation = ""
