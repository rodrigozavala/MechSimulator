from UIElements import SimpleLinkGR, JointGR
from geometric_objects import Line, Point


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
        self.grounded=grounded
        self.line= Line(x0,y0,xf,yf,d,xm,ym,theta)
        

        self.gR=SimpleLinkGR(self.line.getP0Coordinates(),self.line.getPFCoodinates())
        self.currentState="Standard"
        
    
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



class Joint:
    def __init__(self,x,y,links=[]):
        self.links=links
        self.point=Point(x,y)
        self.gR= JointGR(self.point.p)
        self.currentState="Standard"

    def draw(self,pygame,screen):
        self.gR.drawItself(pygame,screen,self.getCurrentState())

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


    
