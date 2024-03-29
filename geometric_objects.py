
import numpy as np
import math
class Point:
    def __init__(self,x,y):
        self.p=np.array([x,y])
        self.x,self.y=x,y

    def setX(self,x):
        self.x=x
        self.p[0]=x

    def setY(self,y):
        self.y=y
        self.p[1]=y

    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
    


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

class Line:
    def __init__(self,x0=None,y0=None,xf=None,yf=None,d=None,xm=None,ym=None,theta=None):
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

    def getP0(self):
        return self.p0


    def getPf(self):
        return self.pf

    def updatepFWithTheta(self, theta):
        self.rotateRespectToP0(theta)

    def updatep0WithTheta(self, theta):
        self.rotateRespectToPF(theta)

    def updateValues(self,p0,theta):
        self.p0 = p0
        self.theta = theta
        #self.pf=Point(self.p0.p[0]+self.d*math.cos(math.radians(self.theta)),self.p0.p[1]+self.d*math.sin(math.radians(self.theta)))
        self.pf=Point(self.p0.p[0]+self.d*math.cos(self.theta),self.p0.p[1]+self.d*math.sin(self.theta))
        self.pm=Point.computeMiddlePoint(self.p0,self.pf)

    def getP0Coordinates(self):
        return self.p0.p
    
    def getPFCoodinates(self):
        return self.pf.p
    
    def getThetaRadians(self):
        return Point.computeAngleRadians(self.p0,self.pf)
    
    def getThetaDegrees(self):
        return Point.computeAngleDegrees(self.p0,self.pf)