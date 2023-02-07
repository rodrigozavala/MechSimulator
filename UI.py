import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import Point,SimpleLink

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
################################

pygame.init()
size=(1000,620)
screen=pygame.display.set_mode(size)
######################################

### About link creation and Mouse use
#### Related to different modes
creationMode=False
#About on click buttons events
i=0
firstTime=True
hasClicked= False

LEFT=1
RIGHT=3
firstPoint=Point(0,0)
lastPoint=Point(0,0)
mousePos=Point(0,0)

objectsInScreen=[]
### About fonts

defFont=pygame.font.get_default_font()
fontSize=10
font=pygame.font.Font(defFont,fontSize)

############# Related to GUI

manager=pygame_gui.UIManager(size)

buttonCreateChar={
"bHeight":75,
"bWidth":150,
"posX":0,
"posY":size[1]-75
}
#Buttons
buttonCreate = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    (buttonCreateChar["posX"],buttonCreateChar["posY"]),(buttonCreateChar["bWidth"],buttonCreateChar["bHeight"])),
    text="Create New Link",manager=manager)

buttonSaveChar = {
    "bHeight":75,
    "bWidth":150,
    "posX":buttonCreateChar["posX"]+buttonCreateChar["bWidth"],
    "posY":size[1]-75
}

buttonSave = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    (buttonSaveChar["posX"],buttonSaveChar["posY"]),(buttonSaveChar["bWidth"],buttonSaveChar["bHeight"])),
    text="Save",manager=manager)



clock=pygame.time.Clock()

while True:
    time_delta=clock.tick(60)/1000.0
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
        elif (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if(event.ui_element == buttonCreate):
                ###set creation mode
                creationMode=True
        elif(creationMode):
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT):
                if(hasClicked):
                    lastPoint.setX(mousePos.p[0])
                    lastPoint.setY(mousePos.p[1])
                    hasClicked=False
                    creationMode=False
                    ###Creating new Link in cartesian way
                    objectsInScreen.append(SimpleLink(firstPoint.getX(),firstPoint.getY(),lastPoint.getX(),lastPoint.getY()))

                elif (not hasClicked):
                    firstPoint.setX(mousePos.p[0])
                    firstPoint.setY(mousePos.p[1])
                    hasClicked=True

            elif(event.type == pygame.KEYDOWN):
                if(event.key ==  pygame.K_TAB):
                    print("Something Activated")

        
        manager.process_events(event)


    #To fill screen background color
    screen.fill(LIGHT_GRAY)

    manager.update(time_delta)

    manager.draw_ui(screen)
    #Animation that must be done if a link is being created
    if (hasClicked):
        distanceBetweenPoints=Point.computeEuclideanDistance(firstPoint,mousePos)
        pygame.draw.line(screen,BLACK,firstPoint.p,mousePos.p,1)
        pygame.draw.circle(screen,BLACK,firstPoint.p,distanceBetweenPoints,1)
        textToDisplay=str(distanceBetweenPoints)
        textSurface=font.render(textToDisplay,True,BLACK)
        screen.blit(textSurface,firstPoint.p+Point.computeMiddlePoint(mousePos,firstPoint).p)
    
    ###Animation to show all objects

    for link in objectsInScreen:
        pygame.draw.line(screen,BLACK,link.p0.p,link.pf.p,5)

    #update screen
    ##This let me show a blue and a red axis
    pygame.draw.line(screen,BLUE,[0,0],[0,100],5)
    pygame.draw.line(screen,RED,[0,0],[100,0],5)

    #pygame.display.flip() #can be used to
    pygame.display.update()
    time.sleep(1/30)

        