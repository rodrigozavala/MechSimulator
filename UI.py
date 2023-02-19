import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import Point,SimpleLink

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
creationMode=False
###################About on click buttons events
i=0
firstTime=True
hasClicked= False

clickTabOnce=False
clickTabTwice=False

LEFT=1
RIGHT=3
firstPoint=Point(0,0)
lastPoint=Point(0,0)
mousePos=Point(0,0)

objectsInScreen=[]
########################### About fonts

defFont=pygame.font.get_default_font()
fontSize=10
fontButtons=pygame.font.Font(defFont,fontSize)

fontInput=pygame.font.Font(defFont,20)

############################################ Related to GUI

manager=pygame_gui.UIManager(size)

buttonCreateChar={
"bHeight":75,
"bWidth":150,
"posX":0,
"posY":size[1]-75
}

##############################Buttons and Buttons characteristics
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

#####################Input text
inputRectangle1Char = {
    "bHeight":40,
    "bWidth":150,
    "posX":buttonSaveChar["posX"]+buttonSaveChar["bWidth"],
    "posY":size[1]-75
}

inputRectangle1=pygame.Rect(inputRectangle1Char["posX"],inputRectangle1Char["posY"],inputRectangle1Char["bWidth"],inputRectangle1Char["bHeight"])

angle_text=""

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
            if(event.ui_element == buttonCreate):##buttonCreate was pressed
                ###set creation mode
                creationMode=True
        elif(creationMode):##creationMode is set True
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

            elif(event.type == pygame.KEYDOWN and hasClicked == True):
                if (clickTabTwice==False and clickTabOnce==False):
                    ##with clickTabTwice==False and clickTabOnce== True we change angle
                    ##with clickTabTwice==True and clickTabOnce== True we change length
                    if(event.key ==  pygame.K_TAB):
                        clickTabOnce = True
                        #https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
                        #print("Something Activated")
                elif (clickTabTwice==False and clickTabOnce== True):#01
                    if(event.key == pygame.K_TAB):
                        clickTabTwice = True
                    elif(event.key == pygame.K_KP_ENTER):
                        clickTabOnce=False
                        clickTabTwice=False
                        hasClicked=False

                elif(clickTabTwice == True and clickTabOnce == True):#11
                    if(event.key == pygame.K_TAB):
                        clickTabTwice = False
                    elif(event.key == pygame.K_KP_ENTER):
                        clickTabOnce=False
                        clickTabTwice=False
                        hasClicked=False





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
    if (hasClicked and clickTabTwice==False and clickTabOnce==False):
        distanceBetweenPoints=Point.computeEuclideanDistance(firstPoint,mousePos)
        pygame.draw.line(screen,BLACK,firstPoint.p,mousePos.p,1)
        pygame.draw.circle(screen,BLACK,firstPoint.p,distanceBetweenPoints,1)
        textToDisplay=str(distanceBetweenPoints)
        textSurface=fontButtons.render(textToDisplay,True,BLACK)
        screen.blit(textSurface,firstPoint.p+Point.computeMiddlePoint(mousePos,firstPoint).p)
        ##I must compute angle and lenght here so input text changes dynamically


    elif (hasClicked and ((clickTabTwice==False and clickTabOnce==True) or (clickTabTwice==True and clickTabOnce==True))):
        ##I must change animation based on lenght and angle here so it works like inventor
        
        pass
    

    #######################Animation to show all objects

    for link in objectsInScreen:
        pygame.draw.line(screen,BLACK,link.p0.p,link.pf.p,5)

    #############################Update screen
    ##This let me show a blue and a red axis
    pygame.draw.line(screen,BLUE,[0,0],[0,100],5)
    pygame.draw.line(screen,RED,[0,0],[100,0],5)

    #pygame.display.flip() #can be used too just like update() below
    pygame.display.update()
    #time.sleep(1/30)

        