import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import Point,SimpleLink
from UIElements import UIButton,UIVariables,Cursor
from EventLogic import EventManager
from Color import Color

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

myCursor=Cursor(0,0,pygame,screen)

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

inputRectangle2Char = {
    "bHeight":40,
    "bWidth":150,
    "posX":UIbuttonSave.getPosX()+UIbuttonSave.getWidth()+150,
    "posY":size[1]-75
}

inputRectangle2=pygame.Rect(inputRectangle2Char["posX"],inputRectangle2Char["posY"],inputRectangle2Char["bWidth"],inputRectangle2Char["bHeight"])

inputRectangle3Char = {
    "bHeight":40,
    "bWidth":150,
    "posX":UIbuttonSave.getPosX()+UIbuttonSave.getWidth()+150+150,
    "posY":size[1]-75
}

inputRectangle3=pygame.Rect(inputRectangle3Char["posX"],inputRectangle3Char["posY"],inputRectangle3Char["bWidth"],inputRectangle3Char["bHeight"])

inputRectangle4Char = {
    "bHeight":40,
    "bWidth":150,
    "posX":UIbuttonSave.getPosX()+UIbuttonSave.getWidth()+150+150+150,
    "posY":size[1]-75
}

inputRectangle4=pygame.Rect(inputRectangle4Char["posX"],inputRectangle4Char["posY"],inputRectangle4Char["bWidth"],inputRectangle4Char["bHeight"])





angle_text=""
user_text=""

user_textX=""
user_textY=""
user_textAngle=""
user_textLenght=""

clock=pygame.time.Clock()
    

myEvents=EventManager(UIElementsDict,objectsInScreen)

while True:
    time_delta=clock.tick(60)/1000.0

    
    for event in pygame.event.get():
        result=myEvents.manageEvents(event)
        if result==0:
            sys.exit()
            break

        manager.process_events(event)

    

    #To fill screen background color
    screen.fill(Color.LIGHT_GRAY.colorCode)
    #To put UI on screen
    myCursor.draw(myEvents.mousePos.getX(),myEvents.mousePos.getY())

    manager.update(time_delta)

    manager.draw_ui(screen)

    pygame.draw.rect(screen,Color.WHITE.colorCode, inputRectangle1)
    pygame.draw.rect(screen,Color.WHITE.colorCode, inputRectangle2)
    pygame.draw.rect(screen,Color.WHITE.colorCode, inputRectangle3)
    pygame.draw.rect(screen,Color.WHITE.colorCode, inputRectangle4)
    


    #Input text on screen
    text_surface = fontInput.render(user_textX, True, (0, 0, 0))
    screen.blit(text_surface, (inputRectangle1.x+100, inputRectangle1.y+5))

    text_surface = fontInput.render(user_textY, True, (0, 0, 0))
    screen.blit(text_surface, (inputRectangle2.x+100, inputRectangle2.y+5))

    text_surface = fontInput.render(user_textAngle, True, (0, 0, 0))
    screen.blit(text_surface, (inputRectangle3.x+100, inputRectangle3.y+5))

    text_surface = fontInput.render(user_textLenght, True, (0, 0, 0))
    screen.blit(text_surface, (inputRectangle4.x+100, inputRectangle4.y+5))

    if(myEvents.creationMode==True):
        if(myEvents.currentState in ["FirstPointCreated","Tab_B1_theta","Tab_B2_long","Enter_B3_long","Enter_B4_theta"] ):
            distanceBetweenPoints=Point.computeEuclideanDistance( myEvents.firstPoint,myEvents.mousePos)
            pygame.draw.line(screen,Color.BLACK.colorCode,myEvents.firstPoint.p,myEvents.mousePos.p,1)
            pygame.draw.circle(screen,Color.BLACK.colorCode,myEvents.firstPoint.p,distanceBetweenPoints,1)
            textToDisplay=str(distanceBetweenPoints)
            textSurface=fontButtons.render(textToDisplay,True,Color.BLACK.colorCode)
            screen.blit(textSurface,myEvents.firstPoint.p+Point.computeMiddlePoint(myEvents.mousePos,myEvents.firstPoint).p)
        
        if(myEvents.currentState =="CreationModeButtonPressed"):
            user_textX=str(myEvents.mousePos.getX())
            user_textY=str(myEvents.mousePos.getY())
            myEvents.inputX=user_textX
            myEvents.inputY=user_textY

        if(myEvents.currentState in ["Tab_A1x","Enter_A4x"]):
            user_textX=myEvents.inputX
            text_surface = fontInput.render(user_text, True, (0, 0, 0))
            screen.blit(text_surface, (inputRectangle1.x+100, inputRectangle1.y+5))
        elif(myEvents.currentState in ["Tab_A2y","Enter_A3y"]):
            user_textY=myEvents.inputY
            text_surface = fontInput.render(user_text, True, (0, 0, 0))
            screen.blit(text_surface, (inputRectangle2.x+100, inputRectangle2.y+5))

        elif(myEvents.currentState in ["Tab_B1_theta","Enter_B4_theta"]):
            pass
        elif(myEvents.currentState in ["Tab_B2_long","Enter_B3_long"]):
            pass

        """
         #Animation that must be done if a link is being created (Creation Mode)
        if (myEvents.hasClicked and myEvents.clickTabTwice==False and myEvents.clickTabOnce==False):

            distanceBetweenPoints=Point.computeEuclideanDistance( myEvents.firstPoint,myEvents.mousePos)
            pygame.draw.line(screen,Color.BLACK.colorCode,myEvents.firstPoint.p,myEvents.mousePos.p,1)
            pygame.draw.circle(screen,Color.BLACK.colorCode,myEvents.firstPoint.p,distanceBetweenPoints,1)
            textToDisplay=str(distanceBetweenPoints)
            textSurface=fontButtons.render(textToDisplay,True,Color.BLACK.colorCode)
            screen.blit(textSurface,myEvents.firstPoint.p+Point.computeMiddlePoint(myEvents.mousePos,myEvents.firstPoint).p)
            ##I must compute angle and lenght here so input text changes dynamically


        elif (myEvents.hasClicked and ((myEvents.changeAngle==True) or (myEvents.changeLength==True))):
            ##I must change animation based on lenght and angle here so it works like inventor
            if(myEvents.changeAngle==True): #01 change length
                    user_text=myEvents.input_text
                    text_surface = fontInput.render(user_text, True, (0, 0, 0))
                    screen.blit(text_surface, (inputRectangle1.x+100, inputRectangle1.y+5))
            elif(myEvents.changeLength==True): #11 change angle
                pass
            pass"""
        





    #######################Animation to show all links

    for link in myEvents.objectsInScreen:
        pygame.draw.line(screen,Color.BLACK.colorCode,link.p0.p,link.pf.p,5)

    #############################Update screen
    ##This let me show a blue and a red axis
    pygame.draw.line(screen,Color.BLUE.colorCode,[0,0],[0,100],5)
    pygame.draw.line(screen,Color.RED.colorCode,[0,0],[100,0],5)

    #pygame.display.flip() #can be used too just like update() below
    pygame.display.update()
    #time.sleep(1/30)



        