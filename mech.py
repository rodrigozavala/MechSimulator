import pygame, sys, time
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import SimpleLink, Point, Mechanism

#Defining variables
t1,t2,t3,t4=sym.symbols("t_1 t_2 t_3 t_4")
w1,w2,w3=sym.symbols("w_1 w_2 w_3")
a1,a2,a3=sym.symbols("a_1 a_2 a_3")
#Defining links long
l1=7
l2=15
l3=7
l4=15 #this is ground

theta1=math.pi*0.312832
omega1=0.3*math.pi
alfa1=0.02
theta4=math.pi*0.5288


angles=[{"theta":((i*0.017453292)+theta1),"omega":omega1,"alfa":alfa1} for i in range(0,39)]
solutions=[[-0.09065,math.pi*1.312832,3.1415*0.03,3.1415*0.3,0,0]]
i=0
for value in angles:
    print("STARTING CALCULATION")
    
    ec1=sym.Eq(l1*sym.cos(t1)+l2*sym.cos(t2)+l3*sym.cos(t3)+l4*sym.cos(t4),0).subs(t4,theta4).subs(t1,value["theta"])
    ec2=sym.Eq(l1*sym.sin(t1)+l2*sym.sin(t2)+l3*sym.sin(t3)+l4*sym.sin(t4),0).subs(t4,theta4).subs(t1,value["theta"])##think if I need to change theta4 after the first simulation
    ##do not change theta4, its ground angle
    
    ec3=sym.Eq(-l1*w1*sym.sin(t1)-l2*w2*sym.sin(t2)-l3*w3*sym.sin(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"])
    ec4=sym.Eq(l1*w1*sym.cos(t1)+l2*w2*sym.cos(t2)+l3*w3*sym.cos(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"])
    
    ec5=sym.Eq(-w1**2*l1*sym.cos(t1)-w2**2*l2*sym.cos(t2)-w3**2*l3*sym.cos(t3)-a1*l1*sym.sin(t1)-a2*l2*sym.sin(t2)-a3*l3*sym.sin(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"]).subs(a1,value["alfa"])
    ec6=sym.Eq(-w1**2*l1*sym.sin(t1)-w2**2*l2*sym.sin(t2)-w3**2*l3*sym.sin(t3)+a1*l1*sym.cos(t1)+a2*l2*sym.cos(t2)+a3*l3*sym.cos(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"]).subs(a1,value["alfa"])
    i+=1
    print(i,solutions[-1])
    something=sym.nsolve([ec1,ec2,ec3,ec4,ec5,ec6],[t2,t3,w2,w3,a2,a3],solutions[-1])##,verify=False)
    solutions.append(something[:])

#Changing angles
solutions = solutions [1:]
#link4Ground.setTheta(theta4)
if(len(angles) == len(solutions)):
    print("AAHHHHHHHHHHHHHH THEY ARE EQUAL IN LENGTH")

else:
    print(len(angles)," ",len(solutions))

"""
for i in len(solutions):
    link1.updatepFWithTheta(angles[i]["theta"])
    link2.setP0(link1.pf)
    link2.updatepFWithTheta(solutions[i][0])
    link3.setP0(link2.pf)
    link3.updatepFWithTheta(solutions[i][1])
    link4Ground.setP0(link3.pf)
"""

#Defining some colors
WHITE=(255,255,255)
CYAN=(0, 251, 255)
BLACK=(0,0,0)
BLUE=(0,0,255)
LIGHT_BLUE=(5, 207, 242)
AQUAMARINE=(35, 184, 169)
RED=(255,0,0)
GREEN=(0,255,0)
LIGHT_PINK=(249, 157, 252)
PINK=(247, 0, 255)
LAVENDER=(199, 135, 245)
VIOLETE=(86, 21, 133)
LILA=(225, 134, 235)
LIGHT_GRAY=(178, 177, 179)
GRAY=(121, 120, 122)
OBSCURE_GRAY=(71, 70, 71)
YELLOW=(240, 232, 5)
ORANGE=(252, 161, 3)
DARK_BROWN=(54, 39, 14)
BROWN=(107, 79, 32)
LIGHT_BRONW=(140, 111, 62)


pygame.init()
size=(800,500)
screen=pygame.display.set_mode(size)

i=0
firstTime=True

hasClicked= False

firstPoint=Point(0,0)
lastPoint=Point(0,0)

mousePos=Point(0,0)

defFont=pygame.font.get_default_font()
fontSize=10
font=pygame.font.Font(defFont,fontSize)
while True:
    for event in pygame.event.get():
        print(event)
        if("pos" in event.__dict__.keys()):
            #print(event.__dict__["pos"][0])
            mousePos.setX(event.__dict__["pos"][0])
            mousePos.setY(event.__dict__["pos"][1])
            #print(mousePos.p[0],mousePos.p[1])
        if(event.type==pygame.QUIT):
            sys.exit()
            break;
        
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            if(hasClicked):
                lastPoint.setX(mousePos.p[0])
                lastPoint.setY(mousePos.p[1])
                hasClicked=False
                
            elif (not hasClicked):
                firstPoint.setX(mousePos.p[0])
                firstPoint.setY(mousePos.p[1])
                hasClicked=True


    #To fill screen background color
    screen.fill(LIGHT_GRAY)

    #This must be done if a link is being created
    if (hasClicked):
        distanceBetweenPoints=Point.computeEuclideanDistance(firstPoint,mousePos)
        pygame.draw.line(screen,BLACK,firstPoint.p,mousePos.p,1)
        pygame.draw.circle(screen,BLACK,firstPoint.p,distanceBetweenPoints,1)
        textToDisplay=str(distanceBetweenPoints)
        textSurface=font.render(textToDisplay,True,BLACK)
        screen.blit(textSurface,firstPoint.p+Point.computeMiddlePoint(mousePos,firstPoint).p)
    
    
    #update screen
    pygame.draw.line(screen,RED,[0,0],[0,100],5)
    pygame.draw.line(screen,RED,[0,0],[100,0],5)


    initx0=200
    inity0=200

    sFactor=10
    if(firstTime):
        link1=SimpleLink(x0=initx0,y0=inity0,d=l1*sFactor,theta=angles[i]["theta"])
        link2=SimpleLink(x0=link1.pf.p[0],y0=link1.pf.p[1],d=l2*sFactor,theta=solutions[i][0])
        link3=SimpleLink(x0=link2.pf.p[0],y0=link2.pf.p[1],d=l3*sFactor,theta=solutions[i][1])
        link4Ground=SimpleLink(x0=link3.pf.p[0],y0=link3.pf.p[1],xf=initx0,yf=inity0,d=l4*sFactor,theta=theta4)
        
        firstTime=False
    
    #Mechanism animation
    th=math.pi*0.5
    link1.updateValues(link1.p0,angles[i]["theta"]+th)
    pygame.draw.line(screen,RED,link1.p0.p,link1.pf.p,5)

    link2.updateValues(link1.pf,solutions[i][0]+th)
    pygame.draw.line(screen,BLACK,link2.p0.p,link2.pf.p,5)

    link3.updateValues(link2.pf,solutions[i][1]+th)
    pygame.draw.line(screen,GREEN,link3.p0.p,link3.pf.p,5)
    
    link4Ground.p0 = link3.pf
    link4Ground.pF = link1.p0
    pygame.draw.line(screen,BROWN,link4Ground.p0.p,link4Ground.pf.p,5)

    i+=1
    if(i==len(solutions)):
        firstTime=True
        i=0
    pygame.display.flip()
    time.sleep(1/30)

        