import pygame, sys, time
import numpy as np
import sympy as sym
from links import SimpleLink

#Defining variables
t1,t2,t3,t4=sym.symbols("t_1 t_2 t_3 t_4")
w1,w2,w3=sym.symbols("w_1 w_2 w_3")
a1,a2,a3=sym.symbols("a_1 a_2 a_3")
#Defining links long
l1=7
l2=15
l3=7
l4=10 #this is ground

theta1=3.1415*0.25
omega1=3.1415*0.3
alfa1=0
theta4=0.5
link1=SimpleLink(d=l1,theta=0.01745329)
link2=SimpleLink(d=l1,theta=0.01745329)
link3=SimpleLink(d=l1,theta=0.01745329)
link4Ground=SimpleLink(d=l1,theta=0.01745329)
angles=[{"theta":(i*0.01745329),"omega":3.1415*0.3,"alfa":0} for i in range(1,361)]
solutions=[[0.7,1,3.1415*0.3,3.1415*0.3,0,0]]
i=0
for value in angles:
    print("STARTING CALCULATION")
    ec1=sym.Eq(l1*sym.cos(t1)+l2*sym.cos(t2)+l3*sym.cos(t3)+l4*sym.cos(t4),0).subs(t4,theta4).subs(t1,value["theta"])
    ec2=sym.Eq(l1*sym.sin(t1)+l2*sym.sin(t2)+l3*sym.sin(t3)+l4*sym.sin(t4),0).subs(t4,theta4).subs(t1,value["theta"])
    ec3=sym.Eq(-l1*w1*sym.sin(t1)-l2*w2*sym.sin(t2)-l3*w3*sym.sin(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"])
    ec4=sym.Eq(l1*w1*sym.cos(t1)+l2*w2*sym.cos(t2)+l3*w3*sym.cos(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"])
    ec5=sym.Eq(-w1**2*l1*sym.cos(t1)-w2**2*l2*sym.cos(t2)-w3**2*l3*sym.cos(t3)-a1*l1*sym.sin(t1)-a2*l2*sym.sin(t2)-a3*l3*sym.sin(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"]).subs(a1,value["alfa"])
    ec6=sym.Eq(-w1**2*l1*sym.sin(t1)-w2**2*l2*sym.sin(t2)-w3**2*l3*sym.sin(t3)+a1*l1*sym.cos(t1)+a2*l2*sym.cos(t2)+a3*l3*sym.cos(t3),0).subs(t1,value["theta"]).subs(w1,value["omega"]).subs(a1,value["alfa"])
    i+=1
    print(i,solutions[-1])
    something=sym.nsolve([ec1,ec2,ec3,ec4,ec5,ec6],[t2,t3,w2,w3,a2,a3],solutions[-1],verify=False)
    #print(something)
    #print(something[:])
    solutions.append(something[:])

print(solutions)
solutions[0]=[]
l=SimpleLink(1,2)
print(l.x0,l.y0)
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
rotation=lambda t: np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
rot=lambda u,t: np.transpose(np.matmul(rotation(t),np.array([[u[0]],[u[1]]])))
rot_point=lambda u,t,p:rot(u-p,t)+p
u0=np.array([0,100])
u1=np.array([200,100])
p=np.array([100,100])

while True:
    for event in pygame.event.get():
        print(event)
        if(event.type==pygame.QUIT):
            sys.exit()
            break;

    
    #to fill screen background color
    screen.fill(LIGHT_GRAY)
    #update screen
    #print("####jajaja")
    pygame.draw.line(screen,GREEN,u0,u1,5)
    pygame.draw.line(screen,RED,[0,0],[0,100],5)
    pygame.draw.line(screen,RED,[0,0],[100,0],5)

    
    #u0=rot(u0,0.05)
    #u0=rot_point(u0,0.05,p)
    #u0=[u0[0,0],u0[0,1]]
    #print(u0)
    
    #u1=rot(u1,0.05)
    #u1=rot_point(u1,0.05,p)
    #u1=[u1[0,0],u1[0,1]]
    #print(u1)
    pygame.display.flip()
    time.sleep(1/30)

        