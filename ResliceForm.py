from PyQt5 import QtWidgets, QtCore, QtGui
import scipy
import scipy.ndimage
import matplotlib.pyplot as plt
from DicomClass import *
from ResliceData import *


class ResliceForm(QtWidgets.QMainWindow):

    dicomData = []
    dicom3d = []
    dicomSize = []
    pos = []
    reslice=[]
    zeroPos=[0,0,0]
    sendMarker=[]
    reSliceData=[]

    def __init__(self,self1, a, b, c,newzero,scaleM,dicomSizeMM,*resliceD, parent=None):
        super(ResliceForm, self).__init__(parent)
        self.initUI()
        # self.reSliceData=ReSliceData(np.asarray(resliceD[1]))
        self.reSliceData=ResliceData(np.reshape(resliceD, [np.shape(resliceD)[1], np.shape(resliceD)[2], np.shape(resliceD)[3]]))
        self.reSliceData.zeroPos = newzero
        self.reSliceData.dicomSize = np.shape(self.reSliceData.dicomData)
        self.reSliceData.reslice = (a, b, c)
        self.reSliceData.pos = (int(self.reSliceData.dicomSize[0] / 2), int(self.reSliceData.dicomSize[1] / 2), int(self.reSliceData.dicomSize[2] / 2))
        self.reSliceData.scaleM=scaleM
        self.reSliceData.dicomSizeMM=dicomSizeMM
        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 0)
        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 1)
        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 2)

    def initUI(self):

        self.setGeometry(20, 50, 1880, 600)
        self.setWindowTitle('Dicom')
        self.statusBar()

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        # img0
        self.img0 = QtWidgets.QLabel(self)
        self.img0.move(20, 50)
        self.img0.resize(600, 400)
        self.img0.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap = QtGui.QPixmap("dicom.png")
        self.img0.setPixmap(pixmap)
        self.img0.setScaledContents(1)
        self.img0.wheelEvent = self.wheelEventImg0Event
        self.img0.mouseDoubleClickEvent = self.DoubleClickEventImg0Event
        # label0
        self.labelImg0 = QtWidgets.QLabel("", self)
        self.labelImg0.move(22, 52)
        self.labelImg0.resize(550, 18)
        self.labelImg0.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg0.setFont(font)

        # img1
        self.img1 = QtWidgets.QLabel(self)
        self.img1.move(640, 50)
        self.img1.resize(600, 400)
        self.img1.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap2 = QtGui.QPixmap("dicom.png")
        self.img1.setPixmap(pixmap2)
        self.img1.setScaledContents(1)
        self.img1.wheelEvent = self.wheelEventImg1Event
        self.img1.mouseDoubleClickEvent = self.DoubleClickEventImg1Event
        # label1
        self.labelImg1 = QtWidgets.QLabel("", self)
        self.labelImg1.move(642, 52)
        self.labelImg1.resize(550, 18)
        self.labelImg1.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg1.setFont(font)

        # img2
        self.img2 = QtWidgets.QLabel(self)
        self.img2.move(1260, 50)
        self.img2.resize(600, 400)
        self.img2.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap3 = QtGui.QPixmap("dicom.png")
        self.img2.setPixmap(pixmap3)
        self.img2.setScaledContents(1)
        self.img2.wheelEvent = self.wheelEventImg2Event
        self.img2.mouseDoubleClickEvent = self.DoubleClickEventImg2Event
        # label1
        self.labelImg2 = QtWidgets.QLabel("", self)
        self.labelImg2.move(1262, 52)
        self.labelImg2.resize(550, 18)
        self.labelImg2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg2.setFont(font)




        self.show()

    @QtCore.pyqtSlot()
    def MainFormEvent(self):
        ''' Give evidence that a bag was punched. '''

        # self.reSliceData.markerFalg=True
        self.reSliceData.markerPos=self.sendMarker
        self.reSliceData.markerFlag = True
        self.reSliceData.pos=self.reSliceData.markerPos
        self.reSliceData.zeroPos=self.reSliceData.markerPos
        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 0)
        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 1)
        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 2)

    def showDialog(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        self.listWidget.clear()
        if fname[0]:
            self.dicomData = DicomClass()
            xx = self.dicomData.DicomSelect(fname)
            for i in range(len(xx)):
                item = QtWidgets.QListWidgetItem(xx[i])
                self.listWidget.addItem(item)

    def LoadData(self):
        value = int(self.listWidget.currentItem().text()[0:2])
        try:
            self.dicomData.DicomRead(value)
            self.dicomData.ct1 = scipy.ndimage.rotate(self.dicomData.ct1, 45, axes=(0, 1), reshape=True,
                                                      output=np.uint8, mode='constant', prefilter=False)
            self.dicomData.ct1 = scipy.ndimage.rotate(self.dicomData.ct1, 45, axes=(0, 2), reshape=True,
                                                      output=np.uint8, order=5, mode='constant', prefilter=False)
            self.dicomData.ct1 = scipy.ndimage.rotate(self.dicomData.ct1, 45, axes=(1, 2), reshape=True,
                                                      output=np.uint8, order=5, mode='constant', prefilter=False)

            self.dicomSize = np.shape(self.dicomData.ct1)

            self.dicom.pos = (int(self.dicomSize[0] / 2), int(self.dicomSize[1] / 2), int(self.dicomSize[2] / 2))
            self.ShowDicom(self.dicomData.ct1, self.dicom.pos, 0)
            self.ShowDicom(self.dicomData.ct1, self.dicom.pos, 1)
            self.ShowDicom(self.dicomData.ct1, self.dicom.pos, 2)

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Dicom Series is not correct')
            msg.exec_()

    def ShowDicom(self, ct, pos, frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        pix0 = self.CreateQPixmap(a0, pos[2], pos[1], self.reSliceData.markerPos[2], self.reSliceData.markerPos[1], 2, 1,self.reSliceData.markerFlag)
        pix1 = self.CreateQPixmap(a1, pos[0], pos[2], self.reSliceData.markerPos[0], self.reSliceData.markerPos[2], 0, 2,self.reSliceData.markerFlag)
        pix2 = self.CreateQPixmap(a2, pos[0], pos[1], self.reSliceData.markerPos[0], self.reSliceData.markerPos[1], 0, 1,self.reSliceData.markerFlag)

        # pix0 = self.CreateQPixmap(a0)

        self.img0.setPixmap(pix0)
        self.img0.setScaledContents(1)
        self.img1.setPixmap(pix1)
        self.img1.setScaledContents(1)
        self.img2.setPixmap(pix2)
        self.img2.setScaledContents(1)
        if frame==0:
            self.labelImg0.setText("(" + str(round((pos[0] - self.reSliceData.zeroPos[0])*self.reSliceData.scaleM[0],2)) + "mm) " +"(" + str(pos[0] - self.reSliceData.zeroPos[0]) + ") " + str(pos[0]) + "/" + str(diSize[0]))
        if frame==1:
            self.labelImg1.setText("(" + str(round((pos[1] - self.reSliceData.zeroPos[1])*self.reSliceData.scaleM[1],2)) + "mm) " +"(" + str(pos[1] - self.reSliceData.zeroPos[1]) + ") " + str(pos[1]) + "/" + str(diSize[1]))
        if frame == 2:
            self.labelImg2.setText("(" + str(round((pos[2] - self.reSliceData.zeroPos[2])*self.reSliceData.scaleM[2],2)) + "mm) " +"(" + str(pos[2] - self.reSliceData.zeroPos[2]) + ") " + str(pos[2]) + "/" + str(diSize[2]))

    def CreateQPixmap(self, data, x1, y1,x2,y2, color1, color2,markerFlag):
        b = np.zeros((np.shape(data)[0], np.shape(data)[1], 3), dtype=np.uint8)
        b[:, :, 0] = data
        b[:, :, 1] = data
        b[:, :, 2] = data
        b[x1, :, color1] = 255
        b[:, y1, color2] = 255

        color3=3-(color1+color2)
        if markerFlag:

            b[x2, y2 - 2, color3] = 255
            b[x2, y2 - 1, color3] = 255
            b[x2, y2, color3] = 255
            b[x2, y2 + 1, color3] = 255
            b[x2, y2 + 2, color3] = 255
            b[x2 - 2, y2, color3] = 255
            b[x2 - 1, y2, color3] = 255
            b[x2 + 1, y2, color3] = 255
            b[x2 + 2, y2, color3] = 255
            # b[x2 -1, y2-1, color3] = 255
            # b[x2 -1, y2+1, color3] = 255
            # b[x2 + 1, y2-1, color3] = 255
            # b[x2 + 1, y2+1, color3] = 255

        img = QtGui.QImage(b, b.shape[1], b.shape[0], b.shape[1] * b.shape[2], QtGui.QImage.Format_RGB888)
        # img = QtGui.QImage(ct[:, :, pos].flatten(), diSize[0], diSize[1], QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(img)
        return pix

    def wheelEventImg0Event(self, event):
        if self.reSliceData is not None:
            if self.reSliceData.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.reSliceData.pos[0] < self.reSliceData.dicomSize[0] - 1):
                        self.reSliceData.pos = (self.reSliceData.pos[0] + 1, self.reSliceData.pos[1], self.reSliceData.pos[2])
                        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.reSliceData.pos[0] > 0):
                        self.reSliceData.pos = (self.reSliceData.pos[0] - 1, self.reSliceData.pos[1], self.reSliceData.pos[2])
                        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 0)

    def wheelEventImg1Event(self, event):
        if self.reSliceData is not None:
            if self.reSliceData.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.reSliceData.pos[1] < self.reSliceData.dicomSize[1] - 1):
                        self.reSliceData.pos = (self.reSliceData.pos[0], self.reSliceData.pos[1] + 1, self.reSliceData.pos[2])
                        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.reSliceData.pos[1] > 0):
                        self.reSliceData.pos = (self.reSliceData.pos[0], self.reSliceData.pos[1] - 1, self.reSliceData.pos[2])
                        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 1)

    def wheelEventImg2Event(self, event):
        if self.reSliceData is not None:
            if self.reSliceData.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.reSliceData.pos[2] < self.reSliceData.dicomSize[2] - 1):
                        self.reSliceData.pos = (self.reSliceData.pos[0], self.reSliceData.pos[1], self.reSliceData.pos[2] + 1)
                        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.reSliceData.pos[2] > 0):
                        self.reSliceData.pos = (self.reSliceData.pos[0], self.reSliceData.pos[1], self.reSliceData.pos[2] - 1)
                        self.ShowDicom(self.reSliceData.dicomData, self.reSliceData.pos, 2)

    def DoubleClickEventImg0Event(self,event):
        if self.reSliceData is not None:
            if self.reSliceData.dicomData != []:
                a0 = np.transpose(self.reSliceData.dicomData[self.reSliceData.pos[0], :, :], (1, 0))
                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg1Event(self,event):
        if self.reSliceData is not None:
            if self.reSliceData.dicomData != []:
                a1 = np.transpose(self.reSliceData.dicomData[:, self.reSliceData.pos[1], :], (0, 1))
                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg2Event(self,event):
        if self.reSliceData is not None:
            if self.reSliceData.dicomData != []:
                a2 = self.reSliceData.dicomData[:, :, self.reSliceData.pos[2]]
                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

