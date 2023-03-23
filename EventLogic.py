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
        elif (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if(event.ui_element == self.UIElements["buttons"]["create"]):##buttonCreate was pressed
                ###set creation mode
                self.creationMode=True
        elif(self.creationMode):##creationMode is set True
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
                if (self.clickTabTwice==False and self.clickTabOnce==False):
                    ##with clickTabTwice==False and clickTabOnce== True we change angle
                    ##with clickTabTwice==True and clickTabOnce== True we change length
                    if(event.key ==  pygame.K_TAB):
                        self.clickTabOnce = True
                        #https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
                        #print("Something Activated")
                elif (self.clickTabTwice==False and self.clickTabOnce== True):#01
                    if(event.key == pygame.K_TAB):
                        self.clickTabTwice = True
                    elif(event.key == pygame.K_KP_ENTER):
                        self.clickTabOnce=False
                        self.clickTabTwice=False
                        self.hasClicked=False

                elif(self.clickTabTwice == True and self.clickTabOnce == True):#11
                    if(event.key == pygame.K_TAB):
                        self.clickTabTwice = False
                    elif(event.key == pygame.K_KP_ENTER):
                        self.clickTabOnce=False
                        self.clickTabTwice=False
                        self.hasClicked=False

        return 1