""""
pyRECaid

Written by:

Pouya Narimani (pouya.narimani@ut.ac.ir).
Hamed Heidari (hamed.h@live.com).

(c) Copyright BCoLab, All Rights Reserved. NO WARRANTY.

"""

class ResliceData():
    dicomData = []
    RawData = []
    dicom3d = []
    dicomSize = []
    pos = []
    zeroPos = (0, 0, 0)
    markerPos = (0, 0, 0)
    markerFlag = False

    def __init__(self, data):
        self.dicomData = data
