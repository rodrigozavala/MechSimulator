from links import Point,SimpleLink
import pygame_gui
import pygame, sys
import math
from Color import Color
from processes import Process, Stage
LEFT=1
RIGHT=3

class EventManager:
    def __init__(self,UIElements,objectsInScreen):
        #self.__events=events
        self.firstPoint=Point(0,0)
        self.lastPoint=Point(0,0)
        self.mousePos=Point(0,0)
        self.creationMode=False
        
        self.hasClicked=False

        self.clickTabTwice=False
        self.clickTabOnce=False

        self.UIElements=UIElements
        self.objectsInScreen=objectsInScreen
        self.input_text=""
        
        self.changeX=False
        self.changeY=False

        self.changeAngle=False
        self.changeLength=False



        self.lineCreationProcess=LineCreationProcess()
        self.userInput=None

        self.inputX="0"
        self.inputY="0"
        self.inputAngle="0"
        self.inputLength="0"

        self.currentState=""

    def manageEvents(self,event):
        print(event)
        if("pos" in event.__dict__.keys()):
            self.mousePos.setX(event.__dict__["pos"][0])
            self.mousePos.setY(event.__dict__["pos"][1])
            
        if(event.type==pygame.QUIT):
            sys.exit()
            return 0
        #################################################### Check buttons pressed
        elif (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if(event.ui_element == self.UIElements["buttons"]["create"]):##buttonCreate was pressed
                ###set creation mode
                self.creationMode=True
            else:
                pass
        ##################################################### Check Modes

        elif(self.creationMode):##creationMode is set True
            #Parse user action into inputs
            if(event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT):
                self.userInput="LClick"
            elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT):
                self.userInput="RClick"
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_TAB):
                self.userInput="Tab_Pressed"
            elif(event.type == pygame.KEYDOWN and event.key == 13):#pygame.K_KP_ENTER):
                self.userInput="Enter_Pressed"
            elif(event.type == pygame.KEYDOWN):
                self.userInput="Typing"
            
            self.currentState=self.lineCreationProcess.getExecutionFlag(event=self.userInput)
            self.userInput="Nothing"
            print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"+self.currentState)
            #"CreationModeButtonPressed"
            #"Tab_A1x" "Tab_A2y" "Enter_A3y" "Enter_A4x"
            #"Tab_B1_theta","Tab_B2_long","Enter_B3_long","Enter_B4_theta"

            if(self.currentState =="CreationModeButtonPressed"):
                self.inputX=str(self.mousePos.getX())
                self.inputY=str(self.mousePos.getY())

            elif(self.currentState =="Tab_A1x"):
                self.changeX=True
                self.changeY=False
                self.inputY=str(self.mousePos.getY())
                self.inputX=self.managing_input_text(event,self.inputX)
                
                
            elif(self.currentState =="Tab_A2y"):
                self.changeX=False
                self.changeY=True
                self.inputX=str(self.mousePos.getX())
                self.inputY=self.managing_input_text(event,self.inputY)
                

            elif(self.currentState == "Enter_A3y"):
                self.changeX=True
                self.changeY=True
                self.inputY=self.managing_input_text(event,self.inputY)
                
            elif(self.currentState == "Enter_A4x"):
                self.changeX=True
                self.changeY=True
                self.inputX=self.managing_input_text(event,self.inputX)
            elif(self.currentState == "FirstPointCreated"):
                self.inputAngle=str(Point.computeAngleDegrees(self.firstPoint,self.mousePos))
                self.inputLength=str(Point.computeEuclideanDistance(self.firstPoint,self.mousePos))

            elif(self.currentState =="Tab_B1_theta"):
                self.changeAngle=True
                self.changeLength=False
                
                self.inputLength=str(Point.computeEuclideanDistance(self.firstPoint,self.mousePos))
                self.inputAngle=self.managing_input_text(event,self.inputAngle)

            elif(self.currentState =="Tab_B2_long"):
                self.changeAngle=False
                self.changeLength=True
                
                self.inputAngle=str(Point.computeAngleDegrees(self.firstPoint,self.mousePos))
                self.inputLength=self.managing_input_text(event,self.inputLength)
                
            elif(self.currentState == "Enter_B3_long"):
                self.changeAngle=True
                self.changeLength=True
                self.inputLength=self.managing_input_text(event,self.inputLength)
            elif(self.currentState == "Enter_B4_theta"):
                self.changeAngle=True
                self.changeLength=True
                self.inputAngle=self.managing_input_text(event,self.inputAngle)
                
            if(self.currentState == "FirstPointCreated" and self.hasClicked==False):

                if(self.changeX==True and self.changeY==True):
                    self.firstPoint.setX(int(self.inputX))
                    self.firstPoint.setY(int(self.inputY))
                elif(self.changeX==True):
                    self.firstPoint.setX(int(self.inputX))
                    self.firstPoint.setY(self.mousePos.p[1])

                elif(self.changeY==True):
                    self.firstPoint.setX(self.mousePos.p[0])
                    self.firstPoint.setY(int(self.inputY))

                else:
                    self.firstPoint.setX(self.mousePos.p[0])
                    self.firstPoint.setY(self.mousePos.p[1])
                
                self.hasClicked=True
                self.clickTabOnce=False
                self.clickTabTwice=False

                self.changeX=False
                self.changeY=False

            elif(self.currentState == "Line_created"):

                if(self.changeAngle==True and self.changeLength==True):
                    self.lastPoint.setX(self.firstPoint.getX()+int(float(self.inputLength)*math.cos(math.radians(float(self.inputAngle)))))
                    self.lastPoint.setY(self.firstPoint.getY()+int(float(self.inputLength)*math.sin(math.radians(float(self.inputAngle)))))
                elif(self.changeAngle==True):
                    distance=Point.computeEuclideanDistance(self.firstPoint,self.mousePos)
                    self.lastPoint.setX(self.firstPoint.getX()+int(distance*math.cos(math.radians(float(self.inputAngle)))))
                    self.lastPoint.setY(self.firstPoint.getY()+int(distance*math.sin(math.radians(float(self.inputAngle)))))

                elif(self.changeLength==True):
                    angle=Point.computeAngleDegrees(self.firstPoint,self.mousePos)
                    self.lastPoint.setX(self.firstPoint.getX()+int(float(self.inputLength)*math.cos(math.radians(angle))))
                    self.lastPoint.setY(self.firstPoint.getY()+int(float(self.inputLength)*math.sin(math.radians(angle))))

                else:
                    self.lastPoint.setX(self.mousePos.p[0])
                    self.lastPoint.setY(self.mousePos.p[1])

                ###Creating new Link in cartesian way
                self.objectsInScreen.append(SimpleLink(self.firstPoint.getX(),self.firstPoint.getY(),self.lastPoint.getX(),self.lastPoint.getY()))
                self.lineCreationProcess.rebootProcess()
                
                self.creationMode=False
                
                self.hasClicked=False
                self.clickTabOnce=False
                self.clickTabTwice=False

                self.changeAngle=False
                self.changeLength=False


        return 1
    
    def managing_input_text(self,event,text):
        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_BACKSPACE and len(text)>0:
                # get text input from 0 to -1 i.e. end.
                if(text =="-0"):
                    return "0"
                text = text[:-1]
                if(text== ""):
                    return "0"
            else:
                if(event.unicode.isnumeric() or (event.unicode == "." and "." not in text) or (event.unicode == "-" and "-" not in text) ):
                    if(text == "0" or text == "-0"):
                        text = text[:-1]
                    text += event.unicode
        if(text== "-"):
            text="-0"
        return text
    
    def getAngle(self):
        return float(self.inputAngle) if (len(self.inputAngle)>0 and self.inputAngle!="-") else 0.0
    
    def getLength(self):
        return float(self.inputLength) if (len(self.inputLength)>0 and self.inputLength!="-") else 0.0



class LineCreationProcess:
    def __init__(self):
        self.creationProcess=Process()
        
        stageA1=Stage()
        stageA2=Stage()
        stageA3=Stage()
        stageA4=Stage()
        stageA5=Stage()

        stageB1=Stage()
        stageB2=Stage()
        stageB3=Stage()
        stageB4=Stage()
        stageB5=Stage()
        
        stageFinalClick=Stage()

        stageA1.setFlag("CreationModeButtonPressed")
        stageA1.addOutputStage("Tab_Pressed",stageA2)
        stageA1.addOutputStage("LClick",stageB1)

        stageA2.setFlag("Tab_A1x")
        stageA2.addOutputStage("Tab_Pressed",stageA3)
        stageA2.addOutputStage("Enter_Pressed",stageA4)
        stageA2.addOutputStage("LClick",stageB1)

        stageA3.setFlag("Tab_A2y")
        stageA3.addOutputStage("Tab_Pressed",stageA2)
        stageA3.addOutputStage("Enter_Pressed",stageA5)
        stageA3.addOutputStage("LClick",stageB1)

        stageA4.setFlag("Enter_A3y")
        stageA4.addOutputStage("Enter_Pressed",stageB1)
        stageA4.addOutputStage("Tab_Pressed",stageA2)
        stageA4.addOutputStage("LClick",stageB1)

        stageA5.setFlag("Enter_A4x")
        stageA5.addOutputStage("Enter_Pressed",stageB1)
        stageA5.addOutputStage("Tab_Pressed",stageA3)
        stageA5.addOutputStage("LClick",stageB1)
        
        stageB1.setFlag("FirstPointCreated")
        stageB1.addOutputStage("Tab_Pressed",stageB2)
        stageB1.addOutputStage("LClick",stageFinalClick)

        stageB2.setFlag("Tab_B1_theta")
        stageB2.addOutputStage("Tab_Pressed",stageB3)
        stageB2.addOutputStage("Enter_Pressed",stageB4)
        stageB2.addOutputStage("LClick",stageFinalClick)

        stageB3.setFlag("Tab_B2_long")
        stageB3.addOutputStage("Tab_Pressed",stageB2)
        stageB3.addOutputStage("Enter_Pressed",stageB5)
        stageB3.addOutputStage("LClick",stageFinalClick)

        stageB4.setFlag("Enter_B3_long")
        stageB4.addOutputStage("Tab_Pressed",stageB2)
        stageB4.addOutputStage("Enter_Pressed",stageFinalClick)
        stageB4.addOutputStage("LClick",stageFinalClick)

        stageB5.setFlag("Enter_B4_theta")
        stageB5.addOutputStage("Tab_Pressed",stageB3)
        stageB5.addOutputStage("Enter_Pressed",stageFinalClick)
        stageB5.addOutputStage("LClick",stageFinalClick)

        stageFinalClick.setFlag("Line_created")

        self.creationProcess.setInitialStage(stageA1)
        self.creationProcess.setFinalStage(stageFinalClick)

        self.creationProcess.addStage(stageA1)
        self.creationProcess.addStage(stageA2)
        self.creationProcess.addStage(stageA3)
        self.creationProcess.addStage(stageA4)
        self.creationProcess.addStage(stageA5)
        self.creationProcess.addStage(stageB1)
        self.creationProcess.addStage(stageB2)
        self.creationProcess.addStage(stageB3)
        self.creationProcess.addStage(stageB4)
        self.creationProcess.addStage(stageB5)
        self.creationProcess.addStage(stageFinalClick)

        self.creationProcess.setCurrentStage(stageA1)

    def getExecutionFlag(self,event):
        self.creationProcess.updateStage(event)
        return self.creationProcess.getCurrentStage().getFlag()
    
    def rebootProcess(self):
        self.creationProcess.rebbot()



class CreationModeLogic:
    def __init__(self, Fonts, UIElements):
        self.UIFonts=Fonts
        self.UIElements = UIElements
        pass

    def creation_mode_logic(self,screen,events,pygame):
        if(events.creationMode==True):
            if(events.currentState in ["FirstPointCreated","Tab_B1_theta","Tab_B2_long","Enter_B3_long","Enter_B4_theta"] ):
                if(events.currentState == "FirstPointCreated" ):
                    distanceBetweenPoints=Point.computeEuclideanDistance( events.firstPoint,events.mousePos)
                    
                    pygame.draw.line(screen,Color.BLACK.colorCode,events.firstPoint.p,events.mousePos.p,1)
                    pygame.draw.circle(screen,Color.BLACK.colorCode,events.firstPoint.p,distanceBetweenPoints,1)

                    textToDisplay=str(distanceBetweenPoints)
                    textSurface=self.UIFonts["fontButtons"].render(textToDisplay,True,Color.BLACK.colorCode)
                    screen.blit(textSurface,events.firstPoint.p+Point.computeMiddlePoint(events.mousePos,events.firstPoint).p)
                    
                    self.UIElements["aux"]["phantomCursor"].position.setX(0)
                    self.UIElements["aux"]["phantomCursor"].position.setY(0)

                    self.UIElements["keyInputs"]["thetaInput"].setInputText(str(Point.computeAngleDegrees(events.firstPoint,events.mousePos)))
                    self.UIElements["keyInputs"]["thetaInput"].showInputText(screen,self.UIFonts["fontInput"])

                    self.UIElements["keyInputs"]["longInput"].setInputText(str(Point.computeEuclideanDistance(events.firstPoint,events.mousePos)))
                    self.UIElements["keyInputs"]["longInput"].showInputText(screen,self.UIFonts["fontInput"])
                    


                elif(events.currentState == "Tab_B1_theta" ):
                    self.UIElements["keyInputs"]["longInput"].setInputText(str(Point.computeEuclideanDistance(events.firstPoint,events.mousePos)))
                    self.UIElements["keyInputs"]["longInput"].showInputText(screen,self.UIFonts["fontInput"])

                    self.UIElements["keyInputs"]["thetaInput"].setInputText(events.inputAngle)
                    self.UIElements["keyInputs"]["thetaInput"].showInputText(screen,self.UIFonts["fontInput"])
                    
                    
                    self.UIElements["aux"]["auxPoint"].setX(events.firstPoint.getX()+int(float(self.UIElements["keyInputs"]["longInput"].getInputText())*math.cos(math.radians(events.getAngle()))))
                    self.UIElements["aux"]["auxPoint"].setY(events.firstPoint.getY()+int(float(self.UIElements["keyInputs"]["longInput"].getInputText())*math.sin(math.radians(events.getAngle()))))

                    pygame.draw.line(screen,Color.BLACK.colorCode,events.firstPoint.p,self.UIElements["aux"]["auxPoint"].p,1)
                    pygame.draw.circle(screen,Color.BLACK.colorCode,events.firstPoint.p,float(self.UIElements["keyInputs"]["longInput"].getInputText()),1)
                    
                
                    
                elif(events.currentState == "Enter_B4_theta"):

                    self.UIElements["keyInputs"]["thetaInput"].setInputText(events.inputAngle)
                    self.UIElements["keyInputs"]["thetaInput"].showInputText(screen,self.UIFonts["fontInput"])

                    self.UIElements["aux"]["auxPoint"].setX(events.firstPoint.getX()+int(float(self.UIElements["keyInputs"]["longInput"].getInputText())*math.cos(math.radians(events.getAngle()))))
                    self.UIElements["aux"]["auxPoint"].setY(events.firstPoint.getY()+int(float(self.UIElements["keyInputs"]["longInput"].getInputText())*math.sin(math.radians(events.getAngle()))))

                    pygame.draw.line(screen,Color.BLACK.colorCode,events.firstPoint.p,self.UIElements["aux"]["auxPoint"].p,1)
                    pygame.draw.circle(screen,Color.BLACK.colorCode,events.firstPoint.p,float(self.UIElements["keyInputs"]["longInput"].getInputText()),1)
                    

                    
                elif(events.currentState == "Tab_B2_long"):
                    self.UIElements["keyInputs"]["thetaInput"].setInputText(str(Point.computeAngleDegrees(events.firstPoint,events.mousePos)))
                    self.UIElements["keyInputs"]["thetaInput"].showInputText(screen,self.UIFonts["fontInput"])

                    self.UIElements["keyInputs"]["longInput"].setInputText(events.inputLength)
                    self.UIElements["keyInputs"]["longInput"].showInputText(screen,self.UIFonts["fontInput"])

                    
                    self.UIElements["aux"]["auxPoint"].setX(events.firstPoint.getX()+int(events.getLength()*math.cos(math.radians(float(self.UIElements["keyInputs"]["thetaInput"].getInputText())))))
                    self.UIElements["aux"]["auxPoint"].setY(events.firstPoint.getY()+int(events.getLength()*math.sin(math.radians(float(self.UIElements["keyInputs"]["thetaInput"].getInputText())))))

                    pygame.draw.line(screen,Color.BLACK.colorCode,events.firstPoint.p,self.UIElements["aux"]["auxPoint"].p,1)
                    pygame.draw.circle(screen,Color.BLACK.colorCode,events.firstPoint.p,events.getLength(),1)
                    

                    
                elif(events.currentState == "Enter_B3_long"):
                    self.UIElements["keyInputs"]["longInput"].setInputText(events.inputLength)
                    self.UIElements["keyInputs"]["longInput"].showInputText(screen,self.UIFonts["fontInput"])

                    self.UIElements["aux"]["auxPoint"].setX(events.firstPoint.getX()+int(float(events.inputLength)*math.cos(math.radians(float(self.UIElements["keyInputs"]["thetaInput"].getInputText())))))
                    self.UIElements["aux"]["auxPoint"].setY(events.firstPoint.getY()+int(float(events.inputLength)*math.sin(math.radians(float(self.UIElements["keyInputs"]["thetaInput"].getInputText())))))

                    pygame.draw.line(screen,Color.BLACK.colorCode,events.firstPoint.p,self.UIElements["aux"]["auxPoint"].p,1)
                    pygame.draw.circle(screen,Color.BLACK.colorCode,events.firstPoint.p,float(self.UIElements["keyInputs"]["longInput"].getInputText()),1)

                    
            if(events.currentState =="CreationModeButtonPressed"):
                self.UIElements["keyInputs"]["xInput"].setInputText(str(events.mousePos.getX()))
                self.UIElements["keyInputs"]["yInput"].setInputText(str(events.mousePos.getY()))
                


            elif(events.currentState == "Tab_A1x"):
                self.UIElements["keyInputs"]["yInput"].setInputText(str(events.mousePos.getY()))

                self.UIElements["aux"]["phantomCursor"].draw(int(self.UIElements["keyInputs"]["xInput"].getInputText()),events.mousePos.p[1])
                
                #Shows vertical line
                pygame.draw.line(screen,Color.BLACK.colorCode,[int(self.UIElements["keyInputs"]["xInput"].getInputText()),0],[int(self.UIElements["keyInputs"]["xInput"].getInputText()),10000],1)
                self.UIElements["keyInputs"]["xInput"].setInputText(events.inputX)
                self.UIElements["keyInputs"]["xInput"].showInputText(screen,self.UIFonts["fontInput"])

            elif(events.currentState == "Enter_A3y"):
                self.UIElements["keyInputs"]["xInput"].setInputText(events.inputX)
                self.UIElements["keyInputs"]["xInput"].showInputText(screen,self.UIFonts["fontInput"])

                self.UIElements["aux"]["phantomCursor"].draw(int(self.UIElements["keyInputs"]["xInput"].getInputText()),int(self.UIElements["keyInputs"]["yInput"].getInputText()))
                
                pygame.draw.line(screen,Color.BLACK.colorCode,[0,int(self.UIElements["keyInputs"]["yInput"].getInputText())],[10000,int(self.UIElements["keyInputs"]["yInput"].getInputText())],1)
                self.UIElements["keyInputs"]["yInput"].setInputText(events.inputY)
                self.UIElements["keyInputs"]["yInput"].showInputText(screen,self.UIFonts["fontInput"])
                
            elif(events.currentState == "Tab_A2y"):
                self.UIElements["keyInputs"]["xInput"].setInputText(str(events.mousePos.getX()))
                self.UIElements["aux"]["phantomCursor"].draw(events.mousePos.p[0],int(self.UIElements["keyInputs"]["yInput"].getInputText()))
                
                #Shows horizontal line
                pygame.draw.line(screen,Color.BLACK.colorCode,[0,int(self.UIElements["keyInputs"]["yInput"].getInputText())],[10000,int(self.UIElements["keyInputs"]["yInput"].getInputText())],1)
                self.UIElements["keyInputs"]["yInput"].setInputText(events.inputY)
                self.UIElements["keyInputs"]["yInput"].showInputText(screen,self.UIFonts["fontInput"])

            elif(events.currentState == "Enter_A4x"):
                self.UIElements["keyInputs"]["yInput"].setInputText(events.inputY)
                self.UIElements["keyInputs"]["yInput"].showInputText(screen,self.UIFonts["fontInput"])

                self.UIElements["aux"]["phantomCursor"].draw(int(self.UIElements["keyInputs"]["xInput"].getInputText()),int(self.UIElements["keyInputs"]["yInput"].getInputText()))

                pygame.draw.line(screen,Color.BLACK.colorCode,[int(self.UIElements["keyInputs"]["xInput"].getInputText()),0],[int(self.UIElements["keyInputs"]["xInput"].getInputText()),10000],1)
                self.UIElements["keyInputs"]["xInput"].setInputText(events.inputX)
                self.UIElements["keyInputs"]["xInput"].showInputText(screen,self.UIFonts["fontInput"])
            
            else:

                pass
        pass