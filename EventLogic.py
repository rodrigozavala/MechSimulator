from links import Point,SimpleLink
import pygame_gui
import pygame, sys

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

        self.inputX=""
        self.inputY=""
        self.inputAngle=""
        self.inputLength=""

        self.currentState=""

    def manageEvents(self,event):
        print(event)
        if("pos" in event.__dict__.keys()):
            #print(event.__dict__["pos"][0])
            self.mousePos.setX(event.__dict__["pos"][0])
            self.mousePos.setY(event.__dict__["pos"][1])
            #print(mousePos.p[0],mousePos.p[1])
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
            if(event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT):
                self.userInput="LClick"
            elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT):
                self.userInput="RClick"
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_TAB):
                self.userInput="Tab_Pressed"
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER):
                self.userInput="Enter_Pressed"
            elif(event.type == pygame.KEYDOWN):
                self.userInput="Typing"
            
            self.currentState=self.lineCreationProcess.getExecutionFlag(event=self.userInput)
            self.userInput="Nothing"
            print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"+self.currentState)
            #"CreationModeButtonPressed"
            #"Tab_A1x" "Tab_A2y" "Enter_A3y" "Enter_A4x"
            #"Tab_B1_theta","Tab_B2_long","Enter_B3_long","Enter_B4_theta"
            if(self.currentState =="Tab_A1x"):
                self.changeX=True
                self.changeY=False
            
                self.clickTabOnce=True
                self.clickTabTwice=False

            elif(self.currentState =="Tab_A2y"):
                self.changeX=False
                self.changeY=True

            elif(self.currentState =="Tab_B1_theta"):
                self.changeAngle=True
                self.changeLength=False

            elif(self.currentState =="Tab_B2_long"):
                self.changeAngle=False
                self.changeLength=True
            
            if(self.currentState == "FirstPointCreated" and self.hasClicked==False):
                self.firstPoint.setX(self.mousePos.p[0])
                self.firstPoint.setY(self.mousePos.p[1])
                
                self.hasClicked=True
                self.clickTabOnce=False
                self.clickTabTwice=False

                self.changeX=False
                self.changeY=False

            elif(self.currentState == "Tab_A1x"):
                self.managing_input_text(event)
                self.inputX=self.input_text
            elif(self.currentState == "Tab_A2y"):
                self.managing_input_text(event)
                self.inputY=self.input_text
            elif(self.currentState == "Enter_A3y"):
                self.inputY=self.input_text
                self.managing_input_text(event)
            elif(self.currentState == "Enter_A4x"):
                self.managing_input_text(event)
                self.inputX=self.input_text
            elif(self.currentState == "Tab_B1_theta"):
                self.managing_input_text(event)
            elif(self.currentState == "Tab_B2_long"):
                self.managing_input_text(event)
            elif(self.currentState == "Enter_B3_long"):
                self.managing_input_text(event)
            elif(self.currentState == "Enter_B4_theta"):
                self.managing_input_text(event)
            elif(self.currentState == "Line_created"):
                self.lastPoint.setX(self.mousePos.p[0])
                self.lastPoint.setY(self.mousePos.p[1])
                self.objectsInScreen.append(SimpleLink(self.firstPoint.getX(),self.firstPoint.getY(),self.lastPoint.getX(),self.lastPoint.getY()))
                self.lineCreationProcess.rebootProcess()
                self.creationMode=False
                self.hasClicked=False
                self.clickTabOnce=False
                self.clickTabTwice=False

            """
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT):
                if(self.hasClicked):
                    self.lastPoint.setX(self.mousePos.p[0])
                    self.lastPoint.setY(self.mousePos.p[1])
                    self.hasClicked=False
                    self.creationMode=False
                    ###Creating new Link in cartesian way
                    self.objectsInScreen.append(SimpleLink(self.firstPoint.getX(),self.firstPoint.getY(),self.lastPoint.getX(),self.lastPoint.getY()))

                elif (not self.hasClicked):
                    self.firstPoint.setX(self.mousePos.p[0])
                    self.firstPoint.setY(self.mousePos.p[1])
                    self.hasClicked=True

            elif(event.type == pygame.KEYDOWN and self.hasClicked == True):
                if (self.clickTabTwice==False and self.clickTabOnce==False):#00
                    ##with clickTabTwice==False and clickTabOnce== True we change angle
                    ##with clickTabTwice==True and clickTabOnce== True we change length
                    if(event.key ==  pygame.K_TAB):
                        self.clickTabOnce = True
                        #https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
                        #print("Something Activated")   
                elif (self.clickTabTwice==False and self.clickTabOnce== True):#01
                    if(event.key == pygame.K_TAB):
                        self.clickTabTwice = True
                        self.changeAngle=False
                    elif(event.key == pygame.K_KP_ENTER):
                        self.clickTabOnce=False
                        self.clickTabTwice=False
                        self.hasClicked=False
                        self.changeAngle=False
                    elif (event.type == pygame.KEYDOWN):
                        self.changeAngle=True
                        self.managing_input_text(event)

                elif(self.clickTabTwice == True and self.clickTabOnce == True):#11
                    if(event.key == pygame.K_TAB):
                        self.clickTabTwice = False
                        self.changeLength=False
                    elif(event.key == pygame.K_KP_ENTER):
                        self.clickTabOnce=False
                        self.clickTabTwice=False
                        self.hasClicked=False
                        self.changeLength=False
                    elif (event.type == pygame.KEYDOWN):
                        self.changeLength=True
                        self.managing_input_text(event)"""

        return 1
    
    def managing_input_text(self,event):
        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_BACKSPACE and len(self.input_text)>0:
                # get text input from 0 to -1 i.e. end.
                self.input_text = self.input_text[:-1]
            else:
                if(event.unicode.isnumeric() or (event.unicode == "." and "." not in self.input_text)):
                    self.input_text += event.unicode



class Stage:
    def __init__(self,output_stages=None,flag=None):
        if(output_stages == None):
            self.output_stages={}
        else:
            self.output_stages=output_stages
        self.flag=flag

    def addOutputStage(self,input,stage):
        self.output_stages[input]=stage

    def validateInput(self,input):
        if (input in self.output_stages.keys()):
            return self.output_stages[input]
        else:
            return self
    
    def getFlag(self):
        return self.flag

    def setFlag(self,flag):
        self.flag=flag

class Process:
    def __init__(self):
        self.stages=[]
        self.initialStage=None
        self.finalStage=None
        self.currentStage=None
        self.nextProcess=None

    
    def addStage(self,stage):
        self.stages.append(stage)

    def setInitialStage(self,stage):
        self.initialStage=stage
        self.currentStage=stage

    def getInitialState(self):
        return self.initialStage

    def setCurrentStage(self,stage):
        self.currentStage=stage

    def getCurrentStage(self):
        return self.currentStage
    
    def setFinalStage(self,stage):
        self.finalStage=stage

    def setNextProcess(self,process):
        self.nextProcess=process
    
    def updateStage(self,input):
        self.currentStage=self.currentStage.validateInput(input)

    def getCurrentStageFlag(self):
        return self.currentStage.getFlag()
    
    def rebbot(self):
        self.currentStage=self.initialStage
    

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
        stageB4.addOutputStage("Enter_Pressed",stageB5)
        stageB4.addOutputStage("LClick",stageFinalClick)

        stageB5.setFlag("Enter_B4_theta")
        stageB5.addOutputStage("Tab_Pressed",stageB2)
        stageB5.addOutputStage("Enter_Pressed",stageB5)
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