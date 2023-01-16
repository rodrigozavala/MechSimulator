import math
import numpy as np



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
        self.grounded=grounded
        if x0 !=None and y0!=None and xf!=None and yf!=None:
            self.p0=Point(x0,y0)
            self.pf=Point(xf,yf)
            self.pm=Point.computeMiddlePoint(self.p0,self.pf)
            self.d=Point.computeEuclideanDistance(self.p0,self.pf)
            self.theta=Point.computeAngleDegrees(self.p0,self.pf)
        elif d!=None and theta!=None:
            self.d=d
            self.theta=theta
            if x0!=None and y0!= None:
                self.p0=Point(x0,y0)
                self.pf=Point(x0+d*math.cos(math.radians(self.theta)),y0+d*math.sin(math.radians(self.theta)))
                self.pm=Point.computeMiddlePoint(self.p0,self.pf)
            elif xm!=None and ym!=None:
                self.pm=Point(xm,ym)
                self.pf=Point(xm+d*math.cos(math.radians(self.theta))/2,ym+d*math.sin(math.radians(self.theta))/2)
                self.p0=Point(xm-d*math.cos(math.radians(self.theta))/2,ym-d*math.sin(math.radians(self.theta))/2)
            elif xf!=None and yf!=None:
                self.pf=Point(xf,yf)
                self.p0=Point(xf-d*math.cos(math.radians(self.theta)),yf-d*math.sin(math.radians(self.theta)))
                self.pm=Point.computeMiddlePoint(self.p0,self.pf)
            else:
                self.p0=Point(0,0)
                self.pf=Point(0,0)
                self.pm=Point(0,0)

 

    def rotateRespectToP0(self,theta):
        delta=theta-self.theta
        self.theta=theta
        rotationMatrix=lambda t: np.array([[np.cos(t)[0],-np.sin(t)[0]],[np.sin(t)[0],np.cos(t)[0]]])
        rot=lambda u,t: np.transpose(np.matmul(rotationMatrix(np.array([t]).astype("float")),np.array([[u[0]],[u[1]]])))
        rot_point=lambda u,t,p:rot(u-p,t)+p
        self.pf.p=rot_point(self.pf.p,delta,self.p0.p)[0]##check this, it seems I have a problem with this
        #self.pf.p=rot_point(self.p0.p,delta,self.pf.p)[0]
        self.pm=Point.computeMiddlePoint(self.p0,self.pf)


    def rotateRespectToPF(self,theta):
        delta=theta-self.theta
        self.theta=theta
        rotationMatrix=lambda t: np.array([[np.cos(t)[0],-np.sin(t)[0]],[np.sin(t)[0],np.cos(t)[0]]])
        rot=lambda u,t: np.transpose(np.matmul(rotationMatrix(np.array([t]).astype("float")),np.array([[u[0]],[u[1]]])))
        rot_point=lambda u,t,p:rot(u-p,t)+p
        self.p0.p=rot_point(self.p0.p,delta,self.pf.p)[0]##check this, it seems I have a problem with this
        self.pm=Point.computeMiddlePoint(self.p0,self.pf)

    
    def setTheta(self, theta):
        self.theta=theta
    
    def setP0(self, p0Prime):
        self.p0 = p0Prime


    def setPf(self, pfPrime):
        self.pf = pfPrime

    def updatepFWithTheta(self, theta):
        self.rotateRespectToP0(theta)

    def updatep0WithTheta(self, theta):
        self.rotateRespectToPF(theta)


class Point:
    def __init__(self,x,y):
        self.p=np.array([x,y])
        self.x,self.y=x,y

    @staticmethod
    def computeEuclideanDistance(p1,p2):
        return np.linalg.norm(p2.p-p1.p)
        #return math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)

    @staticmethod
    def computeMiddlePoint(p1,p2):
        p=(p1.p-p2.p)/2
        return Point(p[0],p[1])
        #return Point((p2.x-p1.x)/2,(p2.y-p1.y)/2)

    @staticmethod
    def computeAngleRadians(p1,p2):
        if p2.p[0]-p1.p[0]==0:
            if p2.p[1]-p1.p[1]==0:
                return 0
            elif p2.p[1]-p1.p[1]>0:
                return 90*math.pi/180
            elif p2.p[1]-p1.p[1]<0:
                return -90*math.pi/180
        #p=(p2.p[1]-p1.p[1])/(p2.p[0]-p1.p[0])
        return math.atan2((p2.p[1]-p1.p[1]),(p2.p[0]-p1.p[0]))
    
    @staticmethod
    def computeAngleDegrees(p1,p2):
        return math.degrees(Point.computeAngleRadians(p1,p2))




        
