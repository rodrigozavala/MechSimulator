import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import SimpleLink, Joint, TJoint
from geometric_objects import Point
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

UIButtonEdit= UIButton("Edit")
UIButtonEdit.setHeight(75).setWidth(150).setPosX(UIbuttonSave.getPosX()).setPosY(UIbuttonCreate.getPosY()-UIbuttonCreate.getHeight())

buttonCreate=UIbuttonCreate.showButton()
buttonSave=UIbuttonSave.showButton()
buttonEdit=UIButtonEdit.showButton()


UIElementsDict["buttons"]={"create":buttonCreate,"save":buttonSave,"edit":buttonEdit}
#####################Input text

inputRectangleX=UIInputTextBar(40,150).setPosX(UIbuttonSave.getPosX()+UIbuttonSave.getWidth()).setPosY(size[1]-75)

inputRectangleY=UIInputTextBar(40,150).setPosX(inputRectangleX.getPosX()+inputRectangleX.getWidth()).setPosY(size[1]-75)

inputRectangleTheta=UIInputTextBar(40,150).setPosX(inputRectangleY.getPosX()+inputRectangleY.getWidth()).setPosY(size[1]-75)

inputRectangleLong=UIInputTextBar(40,150).setPosX(inputRectangleTheta.getPosX()+inputRectangleTheta.getWidth()).setPosY(size[1]-125)

UIElementsDict["keyInputs"]={"xInput":inputRectangleX,"yInput":inputRectangleY,
                             "thetaInput":inputRectangleTheta,"longInput":inputRectangleLong}

angle_text=""
user_text=""


clock=pygame.time.Clock()

##Looks for an image

#imgJoint = pygame.transform.scale(pygame.image.load("Images/1dJoint.png").convert_alpha(),(20,10))


#imgJoint=pygame.transform.rotate(imgJoint,90)

myEvents=EventManager(UIElementsDict,objectsInScreen)
cml=CreationModeLogic(UIFontsDict,UIElementsDict)
myJoint=TJoint(100,100,300,400)
print(myJoint.gR.points)
print(f"length is : {myJoint.gR.lineLength}")
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
    #screen.blit(imgJoint,(100,200))
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

    #Logic of different modes
    
    cml.creation_mode_logic(screen,myEvents,pygame)
        
    #######################Animation to show all links

    #myJoint=Joint(300,300)
    #myJoint.currentState="Warning"
    
    for link in myEvents.objectsInScreen:
        link.draw(pygame,screen)

    #myJoint.draw(pygame,screen)
    myJoint.draw(pygame,screen)
    #############################Update screen
    ##This let me show a blue and a red axis

    pygame.draw.line(screen,Color.BLUE.colorCode,[0,0],[0,100],5)
    pygame.draw.line(screen,Color.RED.colorCode,[0,0],[100,0],5)

    #pygame.display.flip() #can be used too just like update() below
    pygame.display.update()
    
    #time.sleep(1/30)