class ChamberClass:
    xSize=0
    ySize=0
    zSize=0
    xAngle=0
    yAngle=0
    zAngle=0
    xPosition=0
    yPosition=0
    zPosition=0
    chamberSize=[]
    chamberAngle=[]
    chamberPosition=[]


    def __init__(self,xSize,ySize,zSize,xAngle,yAngle,zAngle,xPosition,yPosition,zPosition):
        self.xSize=xSize
        self.ySize=ySize
        self.zSize=zSize
        self.xAngle=xAngle
        self.yAngle=yAngle
        self.zAngle=zAngle
        self.xPosition=xPosition
        self.yPosition=yPosition
        self.zPosition=zPosition
        self.chamberSize=[xSize,ySize,zSize]
        self.chamberAngle=[xAngle,yAngle,zAngle]
        self.chamberPosition=[int(xPosition+(xSize/2)),int(yPosition+(ySize/2)),int(zPosition+(zSize/2))]