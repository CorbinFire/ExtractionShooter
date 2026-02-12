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

class Player(Entity):
    def __init__(self, *args):
        super().__init__(*args)
    def mright(self):
        super().move(3,0)
    def mleft(self):
        super().move(-3,0)
    def mup(self):
        super().move(0,-3)
    def mdown(self):
        super().move(0,3)

class Bullet1(Entity):
    def __init__(self, target, *args):
        self.t=target
        super().__init__(*args)
        self.ID='b1'
    def move(self):
        if distance(self.position(),self.t) > 5:
            super().move(*ratio(self.position(),self.t))
        else:
            Entities.remove(self)


def ratio(a,b):
    run = a[0] - b[0]
    rise = a[1] - b[1]
    return [-10*run/(abs(run)+abs(rise)),-10*rise/(abs(run)+abs(rise))]
def distance(a,b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

P = Player([100,100],'player',[30,30])

Entities = [Entity([600,700],'wasp',[25,25])]

while True:
    time.sleep(0.016)
    wn.fill((255,255,255))
    if pygame.key.get_pressed()[pygame.K_a]:
        P.mleft()
    if pygame.key.get_pressed()[pygame.K_d]:
        P.mright()
    if pygame.key.get_pressed()[pygame.K_w]:
        P.mup()
    if pygame.key.get_pressed()[pygame.K_s]:
        P.mdown()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
    for E in Entities:
        pygame.draw.rect(wn,(150,150,150),E.pos+E.size())
        E.move()
        if E.ID == 'wasp':
            if distance(P.position(),E.position())<200:
                Entities+=[Bullet1(P.position(),E.position(),'',[8,8])]

    pygame.draw.rect(wn,(255,0,0),P.pos+P.size())
    pygame.display.flip()

