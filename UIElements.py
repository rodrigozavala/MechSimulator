
from Color import Color
from links import Point
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
        self.manager=manager##pygame,pygame_gui,manager


class UIButton:
    
    def __init__(self,buttonText="New Button",bHeight=0,bWidth=0,posX=0,posY=0):
        self.__bHeight=bHeight
        self.__bWidth=bWidth
        self.__posX=posX
        self.__posY=posY
        self.__text=buttonText
        self.UIvars=UIVariables()
        self.__pygame_gui=self.UIvars.pygame_gui
        self.__manager=self.UIvars.manager
        self.__pygame=self.UIvars.pygame
        

    def setStaticVariables(self,py,pyg,man):
        self.__pygame_gui=pyg
        self.__manager=man
        self.__pygame=py

   


    def setHeight(self,h):
        self.__bHeight=h
        return self

    def setWidth(self,w):
        self.__bWidth=w
        return self

    def setPosX(self,x):
        self.__posX=x
        return self

    def setPosY(self,y):
        self.__posY=y
        return self

    def getHeight(self):
        return self.__bHeight
    
    def getWidth(self):
        return self.__bWidth

    def getPosX(self):
        return self.__posX
    
    def getPosY(self):
        return self.__posY
    
    def showButton(self):
        return self.__pygame_gui.elements.UIButton(relative_rect=self.__pygame.Rect(
            (self.__posX,self.__posY),(self.__bWidth,self.__bHeight)),text=self.__text,manager=self.__manager)
    

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