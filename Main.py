import pygame
import os
import time
import random
import math


pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
width,hieght = info.current_w,info.current_h
# square_size = [width,width] if width < hieght else [hieght,hieght]
# add_to_each_point = [0,(hieght-width)/2] if width < hieght else [(width-hieght)/2,0]
# rightsidecoverpos = [0,(hieght+width)/2] if width < hieght else [(width+hieght)/2,0]
# sidecoverplus = [width,(hieght-width)/2] if width < hieght else [(width-hieght)/2,hieght]
wn = pygame.display.set_mode([width,hieght])


class Entity:
    def __init__(self,*args):
        self.pos = args[0]
        self.ID = args[1]
        self.s = args[2]
    def position(self):
        return [self.pos[0]+self.s[0]/2,self.pos[1]+self.s[1]/2]
    def size(self):
        return self.s
    def move(self,*args):
        args+=(0,0)
        self.pos = [self.pos[0]+args[0],self.pos[1]+args[1]]

class Wasp(Entity):
    def __init__(self, position, *args):
        self.health = 40
        self.lastshot = 0.1
        self.targets = args[0]
        self.cycle = 0
        super().__init__(position,'wasp',[25,25])
    def move(self):
        if distance(self.position(),self.targets[self.cycle]) < 6:
            self.cycle+=1
            self.cycle%=len(self.targets)
                
        else:
            r = ratio(self.position(),self.targets[self.cycle])
            super().move(r[0]/2,r[1]/2)

class Blob(Entity):
    def __init__(self, position, *args):
        self.health = 40
        self.lastshot = 0.1
        self.targets = args[0]
        self.cycle = 0
        super().__init__(position,'wasp',[50,50])
    def move(self):
        if distance(self.position(),self.targets[self.cycle]) < 6:
            self.cycle+=1
            self.cycle%=len(self.targets)
                
        else:
            r = ratio(self.position(),self.targets[self.cycle])
            super().move(r[0]/2,r[1]/2)

class Player(Entity):
    def __init__(self, *args):
        self.health = 100
        super().__init__(*args)
    def mright(self):
        super().move(3,0)
    def mleft(self):
        super().move(-3,0)
    def mup(self):
        super().move(0,-3)
    def mdown(self):
        super().move(0,3)
    def sright(self):
        super().move(5,0)
    def sleft(self):
        super().move(-5,0)
    def sup(self):
        super().move(0,-5)
    def sdown(self):
        super().move(0,5)

class Bullet1(Entity):
    def __init__(self, target, position, *args):
        super().__init__(position,'b1',[8,8])
        self.r=ratio(self.position(),target)
        self.health = 1

    def move(self):
        if self.position()[0] < 0:
            Entities.remove(self)
        elif self.position()[1] < 0:
            Entities.remove(self)
        elif self.position()[0] > width:
            Entities.remove(self)
        elif self.position()[1] > hieght:
            Entities.remove(self)
            
        elif distance(self.position(),P.position()) < P.size()[0]:
            P.health-=1
            print(P.health)
            # if P.health<0:
                # pygame.quit()
            Entities.remove(self)
                
        else:
            super().move(self.r[0]*2,self.r[1]*2)
            
class pBullet1(Entity):
    def __init__(self, target, position, *args):
        super().__init__(position,'b2',[8,8])
        self.r=ratio(self.position(),target)
        self.health = 1

    def move(self,*args):
        if self.position()[0] < 0:
            Entities.remove(self)
        elif self.position()[1] < 0:
            Entities.remove(self)
        elif self.position()[0] > width:
            Entities.remove(self)
        elif self.position()[1] > hieght:
            Entities.remove(self)
        else:
            firstmove = True
            for E in Entities:            
                if distance(self.position(),E.position()) < E.size()[0] and E.ID != 'b2':
                    E.health-=1
                    print(E.health)
                    if E.health<0:
                        Entities.remove(E)
                    Entities.remove(self)
                    break
                else:
                    if firstmove == True:
                        firstmove = False
                        super().move(self.r[0]*2,self.r[1]*2)

def ratio(a,b):
    run = a[0] - b[0]
    rise = a[1] - b[1]
    return [-10*run/(abs(run)+abs(rise)),-10*rise/(abs(run)+abs(rise))]
def distance(a,b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

P = Player([100,100],'player',[30,30])
Entities = [Wasp([625,725],[[600,700],[1200,800],[1200,40],[350,350]]),Wasp([1500,900],[[600,700],[1200,800],[1200,40],[350,350]]),Wasp([1500,1100],[[600,700],[1200,800],[1200,40],[350,350]])]
running = True

while running:
    time.sleep(0.016)
    AT = time.time()
    wn.fill((255,255,255))
    velocity=[0,0]
    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
        if pygame.key.get_pressed()[pygame.K_a]:
            P.sleft()
            velocity[0]+=5
        if pygame.key.get_pressed()[pygame.K_d]:
            P.sright()
            velocity[0]-=5
        if pygame.key.get_pressed()[pygame.K_w]:
            P.sup()
            velocity[1]+=5
        if pygame.key.get_pressed()[pygame.K_s]:
            P.sdown()
            velocity[1]-=5
    else:
        if pygame.key.get_pressed()[pygame.K_a]:
            P.mleft()
            velocity[0]+=3
        if pygame.key.get_pressed()[pygame.K_d]:
            P.mright()
            velocity[0]-=3
        if pygame.key.get_pressed()[pygame.K_w]:
            P.mup()
            velocity[1]+=3
        if pygame.key.get_pressed()[pygame.K_s]:
            P.mdown()
            velocity[1]-=3
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # Entities+=[pBullet1(pygame.mouse.get_pos(),P.position())]
    for E in Entities:
        pygame.draw.rect(wn,(150,150,150),E.pos+E.size())
        E.move()
        if E.ID == 'wasp':
            if distance(P.position(),E.position())<500 and AT - E.lastshot > .03:
                E.lastshot = AT
                Entities+=[Bullet1([P.position()[0]+velocity[0]*-10+random.randint(-12,12),P.position()[1]+velocity[1]*-10+random.randint(-12,12)],E.position())]
    if pygame.mouse.get_pressed()[0]:
        Entities+=[pBullet1(pygame.mouse.get_pos(),P.position())]
    pygame.draw.rect(wn,(255,0,0),P.pos+P.size())
    pygame.display.flip()

input('Any final words!')
print('Goodbye')