import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import Point,SimpleLink
from UIElements import UIButton, UIVariables, UIInputTextBar, Cursor
from EventLogic import EventManager, CreationModeLogic
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

UIFontsDict={"fontInput":fontInput,"fontButtons":fontButtons}

############################################ Related to GUI

manager=pygame_gui.UIManager(size)

UIVariables().setUIVariables(pygame,pygame_gui,manager)

myCursor=Cursor(0,0,pygame,screen)

phantomCursor=Cursor(0,0,pygame,screen)

auxPoint=Point(0,0)

UIElementsDict={}
UIElementsDict["aux"]={"phantomCursor":phantomCursor,"auxPoint":auxPoint}

##############################Buttons and Buttons characteristics 
UIbuttonCreate= UIButton("Create New Link")

UIbuttonCreate.setHeight(75).setWidth(150).setPosX(0).setPosY(screen.get_size()[1]-UIbuttonCreate.getHeight())

UIbuttonSave=UIButton("Save")
UIbuttonSave.setHeight(75).setWidth(150).setPosX(
    UIbuttonSave.getPosX()+UIbuttonSave.getWidth()).setPosY(screen.get_size()[1]-UIbuttonCreate.getHeight())

buttonCreate=UIbuttonCreate.showButton()
buttonSave=UIbuttonSave.showButton()


UIElementsDict["buttons"]={"create":buttonCreate,"save":buttonSave}
#####################Input text

inputRectangleX=UIInputTextBar(40,150).setPosX(UIbuttonSave.getPosX()+UIbuttonSave.getWidth()).setPosY(size[1]-75)

inputRectangleY=UIInputTextBar(40,150).setPosX(inputRectangleX.getPosX()+inputRectangleX.getWidth()).setPosY(size[1]-75)

inputRectangleTheta=UIInputTextBar(40,150).setPosX(inputRectangleY.getPosX()+inputRectangleY.getWidth()).setPosY(size[1]-75)

inputRectangleLong=UIInputTextBar(40,150).setPosX(inputRectangleTheta.getPosX()+inputRectangleTheta.getWidth()).setPosY(size[1]-125)

UIElementsDict["keyInputs"]={"xInput":inputRectangleX,"yInput":inputRectangleY,
                             "thetaInput":inputRectangleTheta,"longInput":inputRectangleLong}

angle_text=""
user_text=""

#user_textX=""
#user_textY=""
#user_textAngle=""
#user_textLenght=""

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
    #Show rectangles just once
    inputRectangleX.showRectangle(screen)
    inputRectangleY.showRectangle(screen)
    inputRectangleTheta.showRectangle(screen)
    inputRectangleLong.showRectangle(screen)

    #Input text on screen

    inputRectangleX.showInputText(screen,fontInput)
    inputRectangleY.showInputText(screen,fontInput)
    inputRectangleTheta.showInputText(screen,fontInput)
    inputRectangleLong.showInputText(screen,fontInput)

    cml=CreationModeLogic(UIFontsDict,UIElementsDict)
    cml.creation_mode_logic(screen,myEvents,pygame)
        
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



