import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import Point,SimpleLink
from UIElements import UIButton,UIVariables
from EventLogic import EventManager

#############################Defining some colors

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
###############################################

pygame.init()
size=(1000,620)
screen=pygame.display.set_mode(size)

##############################################

########################### About link creation and Mouse use
############################# Related to different modes
###################About on click buttons events
i=0
firstTime=True

objectsInScreen=[]
########################### About fonts

defFont=pygame.font.get_default_font()
fontSize=10
fontButtons=pygame.font.Font(defFont,fontSize)

fontInput=pygame.font.Font(defFont,20)

############################################ Related to GUI

manager=pygame_gui.UIManager(size)



UIVariables().setUIVariables(pygame,pygame_gui,manager)


##############################Buttons and Buttons characteristics 
UIbuttonCreate= UIButton("Create New Link")

UIbuttonCreate.setHeight(75).setWidth(150).setPosX(0).setPosY(screen.get_size()[1]-UIbuttonCreate.getHeight())
UIbuttonSave=UIButton("Save")
UIbuttonSave.setHeight(75).setWidth(150).setPosX(
    UIbuttonSave.getPosX()+UIbuttonSave.getWidth()).setPosY(screen.get_size()[1]-UIbuttonCreate.getHeight())

buttonCreate=UIbuttonCreate.showButton()
buttonSave=UIbuttonSave.showButton()

UIElementsDict={}

UIElementsDict["buttons"]={"create":buttonCreate,"save":buttonSave}
#####################Input text
inputRectangle1Char = {
    "bHeight":40,
    "bWidth":150,
    "posX":UIbuttonSave.getPosX()+UIbuttonSave.getWidth(),
    "posY":size[1]-75
}

inputRectangle1=pygame.Rect(inputRectangle1Char["posX"],inputRectangle1Char["posY"],inputRectangle1Char["bWidth"],inputRectangle1Char["bHeight"])

angle_text=""

clock=pygame.time.Clock()



myEvents=EventManager(UIElementsDict,objectsInScreen)

while True:
    time_delta=clock.tick(60)/1000.0

    
    for event in pygame.event.get():
        result=myEvents.manageEvents(event)
        if result==0:
            break

        manager.process_events(event)


    #To fill screen background color
    screen.fill(LIGHT_GRAY)
    #To put UI on screen
    manager.update(time_delta)

    manager.draw_ui(screen)

    pygame.draw.rect(screen, WHITE, inputRectangle1)


    #Input text on screen
    text_surface = fontInput.render("Hola", True, (0, 0, 0))
    screen.blit(text_surface, (inputRectangle1.x+100, inputRectangle1.y+5))


    #Animation that must be done if a link is being created
    if (myEvents.hasClicked and myEvents.clickTabTwice==False and myEvents.clickTabOnce==False):
        distanceBetweenPoints=Point.computeEuclideanDistance(myEvents.firstPoint,myEvents.mousePos)
        pygame.draw.line(screen,BLACK,myEvents.firstPoint.p,myEvents.mousePos.p,1)
        pygame.draw.circle(screen,BLACK,myEvents.firstPoint.p,distanceBetweenPoints,1)
        textToDisplay=str(distanceBetweenPoints)
        textSurface=fontButtons.render(textToDisplay,True,BLACK)
        screen.blit(textSurface,myEvents.firstPoint.p+Point.computeMiddlePoint(myEvents.mousePos,myEvents.firstPoint).p)
        ##I must compute angle and lenght here so input text changes dynamically


    elif (myEvents.hasClicked and ((myEvents.clickTabTwice==False and myEvents.clickTabOnce==True) or (myEvents.clickTabTwice==True and myEvents.clickTabOnce==True))):
        ##I must change animation based on lenght and angle here so it works like inventor
        
        pass
    

    #######################Animation to show all links

    for link in myEvents.objectsInScreen:
        pygame.draw.line(screen,BLACK,link.p0.p,link.pf.p,5)

    #############################Update screen
    ##This let me show a blue and a red axis
    pygame.draw.line(screen,BLUE,[0,0],[0,100],5)
    pygame.draw.line(screen,RED,[0,0],[100,0],5)

    #pygame.display.flip() #can be used too just like update() below
    pygame.display.update()
    #time.sleep(1/30)

        