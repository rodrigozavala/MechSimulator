import pygame, sys, time
import pygame_gui
import numpy as np
import sympy as sym
import math
import matplotlib.pyplot as plt
from links import Point,SimpleLink
from UIElements import UIButton, UIVariables, UIInputTextBar, Cursor
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

phantomCursor=Cursor(0,0,pygame,screen)

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

inputRectangleX=UIInputTextBar(40,150).setPosX(UIbuttonSave.getPosX()+UIbuttonSave.getWidth()).setPosY(size[1]-75)

inputRectangleY=UIInputTextBar(40,150).setPosX(inputRectangleX.getPosX()+inputRectangleX.getWidth()).setPosY(size[1]-75)

inputRectangleTheta=UIInputTextBar(40,150).setPosX(inputRectangleY.getPosX()+inputRectangleY.getWidth()).setPosY(size[1]-75)

inputRectangleLong=UIInputTextBar(40,150).setPosX(inputRectangleTheta.getPosX()+inputRectangleTheta.getWidth()).setPosY(size[1]-75)


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

    if(myEvents.creationMode==True):
        if(myEvents.currentState in ["FirstPointCreated","Tab_B1_theta","Tab_B2_long","Enter_B3_long","Enter_B4_theta"] ):
            if(myEvents.currentState == "FirstPointCreated" ):
                distanceBetweenPoints=Point.computeEuclideanDistance( myEvents.firstPoint,myEvents.mousePos)
                pygame.draw.line(screen,Color.BLACK.colorCode,myEvents.firstPoint.p,myEvents.mousePos.p,1)
                pygame.draw.circle(screen,Color.BLACK.colorCode,myEvents.firstPoint.p,distanceBetweenPoints,1)

                textToDisplay=str(distanceBetweenPoints)

                textSurface=fontButtons.render(textToDisplay,True,Color.BLACK.colorCode)
                screen.blit(textSurface,myEvents.firstPoint.p+Point.computeMiddlePoint(myEvents.mousePos,myEvents.firstPoint).p)
                phantomCursor.position.setX(0)
                phantomCursor.position.setY(0)


            elif(myEvents.currentState == "Tab_B1_theta" ):
                inputRectangleTheta.setInputText(str(str(myEvents.firstPoint.computeAngleDegrees(myEvents.firstPoint,myEvents.mousePos))))
            
                pass
            elif(myEvents.currentState == "Enter_B4_theta"):

                pass
            elif(myEvents.currentState == "Tab_B2_long"):

                pass
            elif(myEvents.currentState == "Enter_B3_long"):

                pass
        if(myEvents.currentState =="CreationModeButtonPressed"):
            inputRectangleX.setInputText(str(myEvents.mousePos.getX()))
            inputRectangleY.setInputText(str(myEvents.mousePos.getY()))


        elif(myEvents.currentState == "Tab_A1x"):
            inputRectangleY.setInputText(str(myEvents.mousePos.getY()))

            phantomCursor.draw(int(inputRectangleX.getInputText()),myEvents.mousePos.p[1])
            
            #Shows vertical line
            pygame.draw.line(screen,Color.BLACK.colorCode,[int(inputRectangleX.getInputText()),0],[int(inputRectangleX.getInputText()),10000],1)
            inputRectangleX.setInputText(myEvents.inputX)
            inputRectangleX.showInputText(screen,fontInput)

        elif(myEvents.currentState == "Enter_A3y"):
            inputRectangleX.setInputText(myEvents.inputX)
            inputRectangleX.showInputText(screen,fontInput)

            phantomCursor.draw(int(inputRectangleX.getInputText()),int(inputRectangleY.getInputText()))
            
            pygame.draw.line(screen,Color.BLACK.colorCode,[0,int(inputRectangleY.getInputText())],[10000,int(inputRectangleY.getInputText())],1)
            inputRectangleY.setInputText(myEvents.inputY)
            inputRectangleY.showInputText(screen,fontInput)
            
        elif(myEvents.currentState == "Tab_A2y"):
            inputRectangleX.setInputText(str(myEvents.mousePos.getX()))
            phantomCursor.draw(myEvents.mousePos.p[0],int(inputRectangleY.getInputText()))
            
            #Shows horizontal line
            pygame.draw.line(screen,Color.BLACK.colorCode,[0,int(inputRectangleY.getInputText())],[10000,int(inputRectangleY.getInputText())],1)
            inputRectangleY.setInputText(myEvents.inputY)
            inputRectangleY.showInputText(screen,fontInput)

        elif(myEvents.currentState == "Enter_A4x"):
            inputRectangleY.setInputText(myEvents.inputY)
            inputRectangleY.showInputText(screen,fontInput)

            phantomCursor.draw(int(inputRectangleX.getInputText()),int(inputRectangleY.getInputText()))

            pygame.draw.line(screen,Color.BLACK.colorCode,[int(inputRectangleX.getInputText()),0],[int(inputRectangleX.getInputText()),10000],1)
            inputRectangleX.setInputText(myEvents.inputX)
            inputRectangleX.showInputText(screen,fontInput)
        
        else:

            pass
        
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

        