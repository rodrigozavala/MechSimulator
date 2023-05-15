from UIElements import SimpleLinkGR, JointGR
from geometric_objects import Line, Point
import math


class Mechanism:
    """ 
    *links is a list of SimpleLink objects
    *joints is a list of tuples with SimpleLink objects, it defines a Join between certain number of SimpleLink objects
    *JoinTypes is a list of Strings that define the type of joins of Joints
    """
    def __init__(self,links,joins,jointTypes):
        self.links=links[:]
        self.joins=joins[:]
    
    def animateStep(self,vars):
        for i in len(vars):
            if self.links[i].grounded:
                self.links[i].rotateRespectToP0(vars[i])
            else:
                self.links[i].translate(self.links[i-1].pf)
                self.links[i].rotateRespectToP0(vars[i])



class SimpleLink:
    ##I don't have polymorphism here, but passing to other language must be easier than this
    def __init__(self,x0=None,y0=None,xf=None,yf=None,d=None,xm=None,ym=None,theta=None,grounded=False):
        """Please always send x0, y0, xf, yf
        """
        self.grounded = grounded
        self.line = Line(x0,y0,xf,yf,d,xm,ym,theta)
        self.margin = 5
        

        self.gR = SimpleLinkGR(self.line.getP0Coordinates(),self.line.getPFCoodinates())
        self.currentState = "Standard"
        
    
    def rotateRespectToP0(self,theta):
        self.line.rotateRespectToP0(theta)


    def rotateRespectToPF(self,theta):
        self.line.rotateRespectToPF(theta)

    
    def setTheta(self, theta):
        self.line.setTheta(theta)
    
    def setP0(self, p0Prime):
        self.line.setP0(p0Prime)

    def setPf(self, pfPrime):
        self.line.setPf(pfPrime)

    def updatepFWithTheta(self, theta):
        self.line.rotateRespectToP0(theta)

    def updatep0WithTheta(self, theta):
        self.line.rotateRespectToPF(theta)

    def updateValues(self,p0,theta):
        self.line.updateValues(p0,theta)

    def draw(self,pygame,screen):
        self.gR.drawItself(pygame,screen,self.getCurrentState())

    def getCurrentState(self):
        return self.currentState
    
    def setCurrentState(self,currentState):
        self.currentState=currentState


    def updateCurrentState(self,mousePos=None):
        if(mousePos !=None):
            if(self.checkMouseHovering(mousePos)):
                self.currentState="Interaction"
            else:
                self.currentState="Standard"
        else:
            self.currentState="Standard"


    def checkMouseHovering(self,mousePos):
        theta=self.line.getThetaRadians()
        p0=self.line.p0
        pf=self.line.pf

        if(self.line.getThetaDegrees()==90 or self.line.getThetaDegrees()==270
           or self.line.getThetaDegrees()==-270 or self.line.getThetaDegrees()==-90):
            ##logic if link is vertical
            if(mousePos.getX()<=self.margin+p0.getX() and p0.getX()-self.margin<=mousePos.getX()):
                
                if(p0.getY()<pf.getY()):
                    if(mousePos.getY()<=pf.getY()+self.margin and pf.getY()-self.margin<=mousePos.getY()):
                        return True
                else:
                    if(mousePos.getY()<=p0.getY()+self.margin and p0.getY()-self.margin<=mousePos.getY()):
                        return True

        b=(p0.getY()-math.tan(theta)*p0.getX())
        m=math.tan(theta)
        ye=m*mousePos.getX()+b

        if (p0.getX()<=pf.getX()):
            if (p0.getX()-self.margin<=mousePos.getX() and mousePos.getX()<=pf.getX()+self.margin):
                if( mousePos.getY()<ye+self.margin and ye-self.margin<mousePos.getY()):
                    return True
        else:#p0.getX()>pf.getX()
            if (pf.getX()-self.margin<=mousePos.getX() and mousePos.getX()<=p0.getX()+self.margin):
                if(mousePos.getY()<ye+self.margin and ye-self.margin<mousePos.getY()):
                    return True

        return False
        




class Joint:
    def __init__(self,x,y,links=[]):
        self.links=links
        self.point=Point(x,y)
        self.gR= JointGR(self.point.p)
        self.currentState="Standard"
        self.isGrounded=False

    def draw(self,pygame,screen):
        self.gR.drawItself(pygame,screen,self.getCurrentState())

    def addLink(self,link):
        self.links.append(link)

    def getX(self):
        return self.point.getX()
    
    def getY(self):
        return self.point.getY()
    
    def getCoordinates(self):
        return self.point.p
    
    def getCurrentState(self):
        return self.currentState
    
    def setCurrentState(self,currentState):
        self.currentState=currentState

    def updateCurrentState(self,mousePos=None):
        if (len(self.links)<2 and self.isGrounded==False):
            self.currentState="Warning"
            if(mousePos !=None):
                if(self.checkMouseHovering(mousePos)):
                    self.currentState="Interaction"
        else:
            self.currentState="Standard"


    def checkMouseHovering(self,mousePos):
        if(Point.computeEuclideanDistance(mousePos,self.point)<=10):
            return True
        return False
    
