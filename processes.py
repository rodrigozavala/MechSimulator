
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