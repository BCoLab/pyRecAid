
class ResliceData():

    dicomData=[]
    dicom3d=[]
    dicomSize=[]
    pos=[]
    zeroPos=(0,0,0)
    markerPos=(0,0,0)
    markerFlag=False

    def __init__(self,data):
        self.dicomData=data
