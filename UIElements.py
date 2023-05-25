
from Color import Color
import pygame
import numpy as np
from geometric_objects import Point
import math
#class UIVariablesMeta:
#    _instances={}
#    def __call__(self, *args,**kwds):
#        if(self not in self._instances):
#            instance=super().__call__(*args,**kwds)
#            self._instances[self]=instance
#        return self._instances[self]

class UIVariables(object):
    def __new__(self):
        if not hasattr(self,'instance'):
            self.instance=super(UIVariables,self).__new__(self)
        return self.instance
    
    def setUIVariables(self,pygame,pygame_gui,manager):
        self.pygame=pygame
        self.pygame_gui=pygame_gui
        self.manager=manager



class UIRectangularElement:
    def __init__(self,bHeight=0,bWidth=0,posX=0,posY=0):
        self._bHeight=bHeight
        self._bWidth=bWidth
        self._posX=posX
        self._posY=posY
        self.UIvars=UIVariables()
        self._pygame_gui=self.UIvars.pygame_gui
        self._manager=self.UIvars.manager
        self._pygame=self.UIvars.pygame
        

    def setStaticVariables(self,py,pyg,man):
        self._pygame_gui=pyg
        self._manager=man
        self._pygame=py


    def setHeight(self,h):
        self._bHeight=h
        return self

    def setWidth(self,w):
        self._bWidth=w
        return self

    def setPosX(self,x):
        self._posX=x
        return self

    def setPosY(self,y):
        self._posY=y
        return self

    def getHeight(self):
        return self._bHeight
    
    def getWidth(self):
        return self._bWidth

    def getPosX(self):
        return self._posX
    
    def getPosY(self):
        return self._posY


class UIButton(UIRectangularElement):
    
    def __init__(self,buttonText="New Button",bHeight=0,bWidth=0,posX=0,posY=0):
        UIRectangularElement.__init__(self,bHeight,bWidth,posX,posY)
        self._text=buttonText
       
    
    def showButton(self):
        return self._pygame_gui.elements.UIButton(relative_rect=self._pygame.Rect(
            (self._posX,self._posY),(self._bWidth,self._bHeight)),text=self._text,manager=self._manager)


class UIInputTextBar(UIRectangularElement):
    def __init__(self,bHeight=0,bWidth=0,posX=0,posY=0,barColor=Color.WHITE.colorCode,fontSize=10):
        UIRectangularElement.__init__(self,bHeight,bWidth,posX,posY)
        self._color=barColor
        self._fontSize=fontSize
        self._inputText=""

    def setInputText(self,inputText):
        self._inputText = inputText

    def getInputText(self):
        return str(self._inputText)
    
    def appendToInputText(self,inputText):
        self._inputText+=inputText

    def showRectangle(self,screen):
        self._pygame.draw.rect(screen,self._color,self._pygame.Rect(self._posX,self._posY,self._bWidth,self._bHeight))

    def showInputText(self,screen,font):
        text_surface=font.render(self._inputText, True, (0, 0, 0))
        screen.blit(text_surface, (self._posX+100, self._posY+5))


class Cursor:
    def __init__(self,x,y,pygame,screen,scale=1,width=1):
        self.position=Point(x,y)
        self.pygame=pygame
        self.scale=scale
        self.screen=screen
        self.length=10
        self.width=width
        self.initH=Point(self.position.getX()-self.length*self.scale/2,self.position.getY())
        self.endH=Point(self.position.getX()+self.length*self.scale/2,self.position.getY())

        self.initV=Point(self.position.getX(),self.position.getY()-self.length*self.scale/2)
        self.endV=Point(self.position.getX(),self.position.getY()+self.length*self.scale/2)

    
    def setPosition(self,x,y):
        self.position.setX(x)
        self.position.setY(y)

        self.initH.setX(self.position.getX()-self.length*self.scale/2)
        self.initH.setY(self.position.getY())
        self.endH.setX(self.position.getX()+self.length*self.scale/2)
        self.endH.setY(self.position.getY())

        self.initV.setX(self.position.getX())
        self.initV.setY(self.position.getY()-self.length*self.scale/2)
        self.endV.setX(self.position.getX())
        self.endV.setY(self.position.getY()+self.length*self.scale/2)


    def draw(self,x=None,y=None):
        if(x!=None and y!=None):
            self.setPosition(x,y)
        self.pygame.draw.line(self.screen,Color.BLACK.colorCode,self.initH.p,self.endH.p,self.width)
        self.pygame.draw.line(self.screen,Color.BLACK.colorCode,self.initV.p,self.endV.p,self.width)



class GraphicalRepresentation:
    def __init__(self,standarColor,interactionColor,warningColor):
        self.standardColor=standarColor
        self.interactionColor=interactionColor
        self.warningColor=warningColor
        self.currentColor=self.standardColor

    def drawItself(self,pygame,screen,objectState):
        self.currentColor=self.standardColor
        if(objectState == "Warning"):
            self.currentColor=self.warningColor
        elif(objectState == "Interaction"):
            self.currentColor=self.interactionColor


class SimpleLinkGR(GraphicalRepresentation):
    def __init__(self,p0,pf):
        self.standardColor=Color.BLACK.colorCode
        self.interactionColor=Color.GREEN.colorCode
        self.warningColor=Color.YELLOW.colorCode
        self.p0=p0
        self.pf=pf
        self.width=5
        GraphicalRepresentation.__init__(self,self.standardColor,self.interactionColor,self.warningColor)


    def drawItself(self, pygame, screen, objectState):
        super().drawItself(screen,pygame,objectState)
        pygame.draw.line(screen,self.currentColor,self.p0,self.pf,self.width)
        
        #return super().draw(screen, pygame, objectState)

class JointGR(GraphicalRepresentation):
    def __init__(self,p):
        self.standardColor=Color.BLACK.colorCode
        self.interactionColor=Color.GREEN.colorCode
        self.warningColor=Color.YELLOW.colorCode
        self.p=p
        GraphicalRepresentation.__init__(self,self.standardColor,self.interactionColor,self.warningColor)

    def drawItself(self, pygame, screen, objectState):
        super().drawItself(pygame, screen, objectState)
        #pygame.draw.ellipse(screen, self.currentColor, [self.p[0], self.p[1], 8, 8])
        pygame.draw.circle(screen,self.currentColor,self.p,10,2)
        pygame.draw.circle(screen,self.currentColor,self.p,4)
        


class TransJointGR(GraphicalRepresentation):
    def __init__(self,p0,pf):
        self.standardColor=Color.BLACK.colorCode
        self.interactionColor=Color.GREEN.colorCode
        self.warningColor=Color.YELLOW.colorCode
        self.p0=p0
        self.pf=pf
        self.unitImageWidth=20
        self.unitImageHeight=10
        self.width=5
        GraphicalRepresentation.__init__(self,self.standardColor,self.interactionColor,self.warningColor)
        
        theta=Point.computeAngleRadians(self.p0,self.pf)
        thetaAngle=Point.computeAngleDegrees(self.p0,self.pf)

        self.img= pygame.transform.scale(pygame.image.load("Images/1dJoint.png").convert_alpha(),(self.unitImageWidth,self.unitImageHeight))
        self.img=pygame.transform.rotate(self.img,-thetaAngle)

        self.lineLength=Point.computeEuclideanDistance(self.p0,self.pf)
        self.numberUnits=int(self.lineLength/self.unitImageWidth)

        

        if(thetaAngle==90 or thetaAngle==270 or thetaAngle== -90 or thetaAngle== -270):
            self.points=[[self.p0.getX(),self.p0.getY()+i*self.lineLength/self.numberUnits] for i in range(1,self.numberUnits+1)]
        else:
            #b=(p0.getY()-math.tan(theta)*p0.getX())
            m=math.tan(theta)
            self.points=[np.array([1,m])*i*self.lineLength*math.cos(theta)/(self.numberUnits)+np.array([self.p0.getX(),self.p0.getY()]) for i in range(0,self.numberUnits)]
        
        
        
    
    def drawItself(self, pygame, screen, objectState):
        super().drawItself(pygame, screen, objectState)
        #pygame.draw.ellipse(screen, self.currentColor, [self.p[0], self.p[1], 8, 8])
        for p in self.points:
            screen.blit(self.img,p)

        pygame.draw.line(screen,self.currentColor,self.p0.p,self.pf.p,self.width)
        