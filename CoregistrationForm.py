# import os,sys
# import dicom as pydicom
# import numpy as np
# from PyQt5 import  QtGui, QtWidgets, QtCore
from contextlib import contextmanager
# import time
# import matplotlib.pyplot as plt
# import cv2
# import scipy
import scipy.ndimage
# import math
from DicomClass import *
from ResliceForm import *
# from ResliceData import *
# import transforms3d
import Settings

class CoregistrationForm(QtWidgets.QMainWindow):
    hamed=83
    dicom=None
    dicomB=None
    dicomR=None
    signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CoregistrationForm, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.hamed = 1983
        self.setGeometry(20, 50, 1700, 920)
        self.setWindowTitle('Dicom')
        self.statusBar()

        # list
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.move(50, 50)
        self.listWidget.resize(300, 200)

        #button
        self.openDir= QtWidgets.QPushButton("&Load Folder", self)
        self.openDir.move(67, 270)
        self.openDir.clicked.connect(self.LoadDir)

        #button
        self.loadDataButton= QtWidgets.QPushButton("&Load", self)
        self.loadDataButton.move(233, 270)
        self.loadDataButton.clicked.connect(self.LoadData)
        self.loadDataButton.setEnabled(False)

        # list
        self.listWidgetB = QtWidgets.QListWidget(self)
        self.listWidgetB.move(50, 340)
        self.listWidgetB.resize(300, 200)

        #button
        self.openDirB= QtWidgets.QPushButton("&Load Folder", self)
        self.openDirB.move(67, 560)
        self.openDirB.clicked.connect(self.LoadDirB)

        #button
        self.loadDataButtonB= QtWidgets.QPushButton("&Load", self)
        self.loadDataButtonB.move(233, 560)
        self.loadDataButtonB.clicked.connect(self.LoadDataB)
        self.loadDataButtonB.setEnabled(False)

        #button
        self.combineButton= QtWidgets.QPushButton("&CoRegistration", self)
        self.combineButton.move(150, 760)
        self.combineButton.clicked.connect(self.combine)

        #button
        self.sendMainButton= QtWidgets.QPushButton("&Send To MainForm", self)
        self.sendMainButton.move(150, 800)
        self.sendMainButton.clicked.connect(self.sendMain)


        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        # img0
        self.img0 = QtWidgets.QLabel(self)
        self.img0.move(400, 50)
        self.img0.resize(420, 280)
        self.img0.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap = QtGui.QPixmap("dicom.png")
        self.img0.setPixmap(pixmap)
        self.img0.setScaledContents(1)
        self.img0.wheelEvent =self.wheelEventImg0Event
        self.img0.mouseDoubleClickEvent=self.DoubleClickEventImg0Event
        self.img0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImg0 = QtWidgets.QLabel("",self)
        self.labelImg0.move(402,52)
        self.labelImg0.resize(350,18)
        self.labelImg0.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg0.setFont(font)

        # img1
        self.img1 = QtWidgets.QLabel(self)
        self.img1.move(830, 50)
        self.img1.resize(420, 280)
        self.img1.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap2 = QtGui.QPixmap("dicom.png")
        self.img1.setPixmap(pixmap2)
        self.img1.setScaledContents(1)
        self.img1.wheelEvent = self.wheelEventImg1Event
        self.img1.mouseDoubleClickEvent=self.DoubleClickEventImg1Event
        self.img1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImg1 = QtWidgets.QLabel("",self)
        self.labelImg1.move(832,52)
        self.labelImg1.resize(350,18)
        self.labelImg1.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg1.setFont(font)

        # img2
        self.img2 = QtWidgets.QLabel(self)
        self.img2.move(1260, 50)
        self.img2.resize(420, 280)
        self.img2.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap3 = QtGui.QPixmap("dicom.png")
        self.img2.setPixmap(pixmap3)
        self.img2.setScaledContents(1)
        self.img2.wheelEvent = self.wheelEventImg2Event
        self.img2.mouseDoubleClickEvent=self.DoubleClickEventImg2Event
        self.img2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImg2 = QtWidgets.QLabel("",self)
        self.labelImg2.move(1262,52)
        self.labelImg2.resize(350,18)
        self.labelImg2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg2.setFont(font)



        # imgb0
        self.imgb0 = QtWidgets.QLabel(self)
        self.imgb0.move(400, 340)
        self.imgb0.resize(420, 280)
        self.imgb0.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap = QtGui.QPixmap("dicom.png")
        self.imgb0.setPixmap(pixmap)
        self.imgb0.setScaledContents(1)
        self.imgb0.wheelEvent =self.wheelEventImgb0Event
        self.imgb0.mouseDoubleClickEvent=self.DoubleClickEventImgb0Event
        self.imgb0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImgb0 = QtWidgets.QLabel("",self)
        self.labelImgb0.move(402,342)
        self.labelImgb0.resize(350,18)
        self.labelImgb0.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgb0.setFont(font)

        # imgb1
        self.imgb1 = QtWidgets.QLabel(self)
        self.imgb1.move(830, 340)
        self.imgb1.resize(420, 280)
        self.imgb1.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap2 = QtGui.QPixmap("dicom.png")
        self.imgb1.setPixmap(pixmap2)
        self.imgb1.setScaledContents(1)
        self.imgb1.wheelEvent = self.wheelEventImgb1Event
        self.imgb1.mouseDoubleClickEvent=self.DoubleClickEventImgb1Event
        self.imgb1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgb1 = QtWidgets.QLabel("",self)
        self.labelImgb1.move(832,342)
        self.labelImgb1.resize(350,18)
        self.labelImgb1.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgb1.setFont(font)

        # imgb2
        self.imgb2 = QtWidgets.QLabel(self)
        self.imgb2.move(1260, 340)
        self.imgb2.resize(420, 280)
        self.imgb2.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap3 = QtGui.QPixmap("dicom.png")
        self.imgb2.setPixmap(pixmap3)
        self.imgb2.setScaledContents(1)
        self.imgb2.wheelEvent = self.wheelEventImgb2Event
        self.imgb2.mouseDoubleClickEvent=self.DoubleClickEventImgb2Event
        self.imgb2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgb2 = QtWidgets.QLabel("",self)
        self.labelImgb2.move(1262,342)
        self.labelImgb2.resize(350,18)
        self.labelImgb2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgb2.setFont(font)


        # imgc0
        self.imgc0 = QtWidgets.QLabel(self)
        self.imgc0.move(400, 630)
        self.imgc0.resize(420, 280)
        self.imgc0.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap = QtGui.QPixmap("dicom.png")
        self.imgc0.setPixmap(pixmap)
        self.imgc0.setScaledContents(1)
        self.imgc0.wheelEvent =self.wheelEventImgc0Event
        self.imgc0.mouseDoubleClickEvent=self.DoubleClickEventImgc0Event
        self.imgc0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImgc0 = QtWidgets.QLabel("",self)
        self.labelImgc0.move(402,632)
        self.labelImgc0.resize(350,18)
        self.labelImgc0.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgc0.setFont(font)

        # imgc1
        self.imgc1 = QtWidgets.QLabel(self)
        self.imgc1.move(830, 630)
        self.imgc1.resize(420, 280)
        self.imgc1.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap2 = QtGui.QPixmap("dicom.png")
        self.imgc1.setPixmap(pixmap2)
        self.imgc1.setScaledContents(1)
        self.imgc1.wheelEvent = self.wheelEventImgc1Event
        self.imgc1.mouseDoubleClickEvent=self.DoubleClickEventImgc1Event
        self.imgc1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgc1 = QtWidgets.QLabel("",self)
        self.labelImgc1.move(832,632)
        self.labelImgc1.resize(350,18)
        self.labelImgc1.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgc1.setFont(font)

        # imgc2
        self.imgc2 = QtWidgets.QLabel(self)
        self.imgc2.move(1260, 630)
        self.imgc2.resize(420, 280)
        self.imgc2.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap3 = QtGui.QPixmap("dicom.png")
        self.imgc2.setPixmap(pixmap3)
        self.imgc2.setScaledContents(1)
        self.imgc2.wheelEvent = self.wheelEventImgc2Event
        self.imgc2.mouseDoubleClickEvent=self.DoubleClickEventImgc2Event
        self.imgc2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgc2 = QtWidgets.QLabel("",self)
        self.labelImgc2.move(1262,632)
        self.labelImgc2.resize(350,18)
        self.labelImgc2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgc2.setFont(font)


        # region ReSlice
        # group box
        self.groupBox = QtWidgets.QGroupBox('&Impact option', self)
        self.groupBox.move(67, 650)
        self.groupBox.resize(266, 60)

        #spinbox
        # self.spinboxLabel0 = QtWidgets.QLabel("X:", self.groupBox)
        # self.spinboxLabel0.move(20, 25)
        # self.spinbox0 = QtWidgets.QSpinBox(self.groupBox)
        # self.spinbox0.move(40, 25)
        # self.spinbox0.setMinimum(-180)
        # self.spinbox0.setMaximum(180)
        # self.spinbox0.setValue(0)

        self.spinboxLabel1 = QtWidgets.QLabel("Image 1:", self.groupBox)
        self.spinboxLabel1.move(5, 25)
        self.spinbox1 = QtWidgets.QSpinBox(self.groupBox)
        self.spinbox1.move(55, 23)
        self.spinbox1.setMinimum(0)
        self.spinbox1.setMaximum(100)
        self.spinbox1.setValue(0)

        self.spinboxLabel2 = QtWidgets.QLabel("Image 2:", self.groupBox)
        self.spinboxLabel2.move(130, 25)
        self.spinbox2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinbox2.move(190, 23)
        self.spinbox2.setMinimum(0)
        self.spinbox2.setMaximum(100)
        self.spinbox2.setValue(0)


        #menu
        openFile = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.LoadDir)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

    @contextmanager
    def WaitCursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def LoadDir(self):
        fname =QtWidgets.QFileDialog.getExistingDirectory()
        try:
            with self.WaitCursor():
                if fname[0]:
                    self.listWidget.clear()
                    self.dicom = DicomClass()
                    xx=self.dicom.DicomSelect(fname)
                    for i in range(len(xx)):
                        item = QtWidgets.QListWidgetItem(xx[i])
                        self.listWidget.addItem(item)
                if (~self.loadDataButton.isEnabled()):
                    self.loadDataButton.setEnabled(True)
                self.mainform.dicom=[]
        except:
            time.sleep(0.001)

    def LoadDirB(self):
        fname =QtWidgets.QFileDialog.getExistingDirectory()
        try:
            with self.WaitCursor():
                if fname[0]:
                    self.listWidgetB.clear()
                    self.dicomB = DicomClass()
                    xx=self.dicomB.DicomSelect(fname)
                    for i in range(len(xx)):
                        item = QtWidgets.QListWidgetItem(xx[i])
                        self.listWidgetB.addItem(item)
                if (~self.loadDataButtonB.isEnabled()):
                    self.loadDataButtonB.setEnabled(True)
        except:
            time.sleep(0.001)

    def LoadData(self):
        value = int(self.listWidget.currentItem().text()[0:2])
        try:
            with self.WaitCursor():
                self.dicom.DicomRead(value,1)
                # self.dicom.dicomSize=np.shape(self.dicom.dicomData)
                self.dicom.pos=(int(self.dicom.dicomSizePixel[0] / 2), int(self.dicom.dicomSizePixel[1] / 2), int(self.dicom.dicomSizePixel[2] / 2))
                self.dicom.zeroPos=(0,0,0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Dicom Series is not correct')
            msg.exec_()

    def LoadDataB(self):
        value = int(self.listWidgetB.currentItem().text()[0:2])
        try:
            with self.WaitCursor():
                self.dicomB.DicomRead(value,1)

                # self.dicom.dicomSize=np.shape(self.dicom.dicomData)
                self.dicomB.pos=(int(self.dicomB.dicomSizePixel[0] / 2), int(self.dicomB.dicomSizePixel[1] / 2), int(self.dicomB.dicomSizePixel[2] / 2))
                self.dicomB.zeroPos=(0,0,0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Dicom Series is not correct')
            msg.exec_()

    def ShowDicom(self,ct,pos,frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        pix0 = self.CreateQPixmap(a0, round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]),
                                  round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]), pos[2], pos[1], self.dicom.markerPos[2], self.dicom.markerPos[1], 2, 1, self.dicom.markerFlag)
        pix1 = self.CreateQPixmap(a1, round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                  round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]), pos[0], pos[2], self.dicom.markerPos[0], self.dicom.markerPos[2], 0, 2, self.dicom.markerFlag)
        pix2 = self.CreateQPixmap(a2, round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                  round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]), pos[0], pos[1], self.dicom.markerPos[0], self.dicom.markerPos[1], 0, 1, self.dicom.markerFlag)
        self.img0.setPixmap(pix0)
        self.img0.setScaledContents(1)
        self.img1.setPixmap(pix1)
        self.img1.setScaledContents(1)
        self.img2.setPixmap(pix2)
        self.img2.setScaledContents(1)
        if frame==0:
            self.labelImg0.setText("(" + str(round((pos[0] - self.dicom.zeroPos[0])*self.dicom.scaleM[0],2)) + "mm) " + str(round(pos[0] * self.dicom.scaleM[0], 2)) + "mm /" + str(self.dicom.dicomSizeMM[0])+"mm")
        if frame==1:
            self.labelImg1.setText("(" + str(round((pos[1] - self.dicom.zeroPos[1])*self.dicom.scaleM[1],2)) + "mm) " + str(round(pos[1] * self.dicom.scaleM[1], 2)) + "mm /" + str(self.dicom.dicomSizeMM[1])+"mm")
        if frame == 2:
            self.labelImg2.setText("(" + str(round((pos[2] - self.dicom.zeroPos[2])*self.dicom.scaleM[2],2)) + "mm) " + str(round(pos[2] * self.dicom.scaleM[2], 2)) + "mm /" + str(self.dicom.dicomSizeMM[2])+"mm")

    def ShowDicomB(self,ct,pos,frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        pix0 = self.CreateQPixmap(a0, round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]),
                                  round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]), pos[2], pos[1], self.dicomB.markerPos[2], self.dicomB.markerPos[1], 2, 1, self.dicomB.markerFlag)
        pix1 = self.CreateQPixmap(a1, round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0]),
                                  round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]), pos[0], pos[2], self.dicomB.markerPos[0], self.dicomB.markerPos[2], 0, 2, self.dicomB.markerFlag)
        pix2 = self.CreateQPixmap(a2, round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0]),
                                  round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]), pos[0], pos[1], self.dicomB.markerPos[0], self.dicomB.markerPos[1], 0, 1, self.dicomB.markerFlag)
        self.imgb0.setPixmap(pix0)
        self.imgb0.setScaledContents(1)
        self.imgb1.setPixmap(pix1)
        self.imgb1.setScaledContents(1)
        self.imgb2.setPixmap(pix2)
        self.imgb2.setScaledContents(1)
        if frame==0:
            self.labelImgb0.setText("(" + str(round((pos[0] - self.dicomB.zeroPos[0])*self.dicomB.scaleM[0],2)) + "mm) " + str(round(pos[0] * self.dicomB.scaleM[0], 2)) + "mm /" + str(self.dicomB.dicomSizeMM[0])+"mm")
        if frame==1:
            self.labelImgb1.setText("(" + str(round((pos[1] - self.dicomB.zeroPos[1])*self.dicomB.scaleM[1],2)) + "mm) " + str(round(pos[1] * self.dicomB.scaleM[1], 2)) + "mm /" + str(self.dicomB.dicomSizeMM[1])+"mm")
        if frame == 2:
            self.labelImgb2.setText("(" + str(round((pos[2] - self.dicomB.zeroPos[2])*self.dicomB.scaleM[2],2)) + "mm) " + str(round(pos[2] * self.dicomB.scaleM[2], 2)) + "mm /" + str(self.dicomB.dicomSizeMM[2])+"mm")

    def ShowDicomR(self, ct, pos, frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        pix0 = self.CreateQPixmap(a0, round(self.dicomR.scale[1] * self.dicomR.dicomSizePixel[1]),
                                  round(self.dicomR.scale[2] * self.dicomR.dicomSizePixel[2]), pos[2], pos[1],
                                  self.dicomR.markerPos[2], self.dicomR.markerPos[1], 2, 1, self.dicomR.markerFlag)
        pix1 = self.CreateQPixmap(a1, round(self.dicomR.scale[0] * self.dicomR.dicomSizePixel[0]),
                                  round(self.dicomR.scale[2] * self.dicomR.dicomSizePixel[2]), pos[0], pos[2],
                                  self.dicomR.markerPos[0], self.dicomR.markerPos[2], 0, 2, self.dicomR.markerFlag)
        pix2 = self.CreateQPixmap(a2, round(self.dicomR.scale[0] * self.dicomR.dicomSizePixel[0]),
                                  round(self.dicomR.scale[1] * self.dicomR.dicomSizePixel[1]), pos[0], pos[1],
                                  self.dicomR.markerPos[0], self.dicomR.markerPos[1], 0, 1, self.dicomR.markerFlag)
        self.imgc0.setPixmap(pix0)
        self.imgc0.setScaledContents(1)
        self.imgc1.setPixmap(pix1)
        self.imgc1.setScaledContents(1)
        self.imgc2.setPixmap(pix2)
        self.imgc2.setScaledContents(1)
        if frame == 0:
            self.labelImgc0.setText(
                "(" + str(round((pos[0] - self.dicomR.zeroPos[0]) * self.dicomR.scaleM[0], 2)) + "mm) " + str(
                    round(pos[0] * self.dicomR.scaleM[0], 2)) + "mm /" + str(self.dicomR.dicomSizeMM[0]) + "mm")
        if frame == 1:
            self.labelImgc1.setText(
                "(" + str(round((pos[1] - self.dicomR.zeroPos[1]) * self.dicomR.scaleM[1], 2)) + "mm) " + str(
                    round(pos[1] * self.dicomR.scaleM[1], 2)) + "mm /" + str(self.dicomR.dicomSizeMM[1]) + "mm")
        if frame == 2:
            self.labelImgc2.setText(
                "(" + str(round((pos[2] - self.dicomR.zeroPos[2]) * self.dicomR.scaleM[2], 2)) + "mm) " + str(
                    round(pos[2] * self.dicomR.scaleM[2], 2)) + "mm /" + str(self.dicomR.dicomSizeMM[2]) + "mm")

    def CreateQPixmap(self,data,scl0,scl1,x1,y1,x2,y2,color1,color2,markerFlag):
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
        pix = pix.scaled(scl0, scl1)
        return pix

    def wheelEventImg0Event(self,event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicom.pos[0] < self.dicom.dicomSizePixel[0]-1):
                        self.dicom.pos = (self.dicom.pos[0] + 1, self.dicom.pos[1], self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[0] > 0):
                        self.dicom.pos = (self.dicom.pos[0] - 1, self.dicom.pos[1], self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 0)

    def wheelEventImg1Event(self,event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicom.pos[1] < self.dicom.dicomSizePixel[1]-1):
                        self.dicom.pos = (self.dicom.pos[0] , self.dicom.pos[1]+ 1, self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[1] > 0):
                        self.dicom.pos = (self.dicom.pos[0] , self.dicom.pos[1]- 1, self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 1)

    def wheelEventImg2Event(self,event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicom.pos[2] < self.dicom.dicomSizePixel[2]-1):
                        self.dicom.pos = (self.dicom.pos[0] , self.dicom.pos[1], self.dicom.pos[2]+ 1)
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[2] > 0):
                        self.dicom.pos = (self.dicom.pos[0] , self.dicom.pos[1], self.dicom.pos[2]- 1)
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 2)

    def DoubleClickEventImg0Event(self,event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a0 = np.transpose(self.dicom.dicomData[self.dicom.pos[0], :, :], (1, 0))
                a0=cv2.resize(a0, (round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]).astype(int), round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg1Event(self,event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a1 = np.transpose(self.dicom.dicomData[:, self.dicom.pos[1], :], (0, 1))
                a1=cv2.resize(a1, (round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]).astype(int), round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg2Event(self,event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a2 = self.dicom.dicomData[:, :, self.dicom.pos[2]]
                a2=cv2.resize(a2, (round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]).astype(int), round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def wheelEventImgb0Event(self,event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicomB.pos[0] < self.dicomB.dicomSizePixel[0]-1):
                        self.dicomB.pos = (self.dicomB.pos[0] + 1, self.dicomB.pos[1], self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicomB.pos[0] > 0):
                        self.dicomB.pos = (self.dicomB.pos[0] - 1, self.dicomB.pos[1], self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 0)

    def wheelEventImgb1Event(self,event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicomB.pos[1] < self.dicomB.dicomSizePixel[1]-1):
                        self.dicomB.pos = (self.dicomB.pos[0] , self.dicomB.pos[1]+ 1, self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicomB.pos[1] > 0):
                        self.dicomB.pos = (self.dicomB.pos[0] , self.dicomB.pos[1]- 1, self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 1)

    def wheelEventImgb2Event(self,event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicomB.pos[2] < self.dicomB.dicomSizePixel[2]-1):
                        self.dicomB.pos = (self.dicomB.pos[0] , self.dicomB.pos[1], self.dicomB.pos[2]+ 1)
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicomB.pos[2] > 0):
                        self.dicomB.pos = (self.dicomB.pos[0] , self.dicomB.pos[1], self.dicomB.pos[2]- 1)
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 2)

    def DoubleClickEventImgb0Event(self,event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                a0 = np.transpose(self.dicomB.dicomData[self.dicomB.pos[0], :, :], (1, 0))
                a0=cv2.resize(a0, (round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]).astype(int), round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgb1Event(self,event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                a1 = np.transpose(self.dicomB.dicomData[:, self.dicomB.pos[1], :], (0, 1))
                a1=cv2.resize(a1, (round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0]).astype(int), round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgb2Event(self,event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                a2 = self.dicomB.dicomData[:, :, self.dicomB.pos[2]]
                a2=cv2.resize(a2, (round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0]).astype(int), round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def wheelEventImgc0Event(self,event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicomR.pos[0] < self.dicomR.dicomSizePixel[0]-1):
                        self.dicomR.pos = (self.dicomR.pos[0] + 1, self.dicomR.pos[1], self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicomR.pos[0] > 0):
                        self.dicomR.pos = (self.dicomR.pos[0] - 1, self.dicomR.pos[1], self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 0)

    def wheelEventImgc1Event(self,event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicomR.pos[1] < self.dicomR.dicomSizePixel[1]-1):
                        self.dicomR.pos = (self.dicomR.pos[0] , self.dicomR.pos[1]+ 1, self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicomR.pos[1] > 0):
                        self.dicomR.pos = (self.dicomR.pos[0] , self.dicomR.pos[1]- 1, self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 1)

    def wheelEventImgc2Event(self,event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                numPixels =event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y()>0):
                    if (self.dicomR.pos[2] < self.dicomR.dicomSizePixel[2]-1):
                        self.dicomR.pos = (self.dicomR.pos[0] , self.dicomR.pos[1], self.dicomR.pos[2]+ 1)
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicomR.pos[2] > 0):
                        self.dicomR.pos = (self.dicomR.pos[0] , self.dicomR.pos[1], self.dicomR.pos[2]- 1)
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 2)

    def DoubleClickEventImgc0Event(self,event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                a0 = np.transpose(self.dicomR.dicomData[self.dicomR.pos[0], :, :], (1, 0))
                a0=cv2.resize(a0, (round(self.dicomR.scale[1] * self.dicomR.dicomSizePixel[1]).astype(int), round(self.dicomR.scale[2] * self.dicomR.dicomSizePixel[2]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgc1Event(self,event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                a1 = np.transpose(self.dicomR.dicomData[:, self.dicomR.pos[1], :], (0, 1))
                a1=cv2.resize(a1, (round(self.dicomR.scale[0] * self.dicomR.dicomSizePixel[0]).astype(int), round(self.dicomR.scale[2] * self.dicomR.dicomSizePixel[2]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgc2Event(self,event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                a2 = self.dicomR.dicomData[:, :, self.dicomR.pos[2]]
                a2=cv2.resize(a2, (round(self.dicomR.scale[0] * self.dicomR.dicomSizePixel[0]).astype(int), round(self.dicomR.scale[1] * self.dicomR.dicomSizePixel[1]).astype(int)), interpolation = cv2.INTER_AREA)
                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def combine(self):
        if ((self.dicom is not None)and(self.dicomB is not None)):
            with self.WaitCursor():
                a=self.dicom.pos
                b=np.subtract(self.dicom.dicomSizePixel,self.dicom.pos)
                c=self.dicomB.pos
                d = np.subtract(self.dicomB.dicomSizePixel,self.dicomB.pos)
                x=np.maximum(a,c)
                z=np.maximum(b,d)
                newD1=np.zeros((x[0]+z[0],x[1]+z[1],x[2]+z[2]))
                newD2 = np.zeros((x[0] + z[0], x[1] + z[1], x[2] + z[2]))
                start1 =np.subtract(x,a)
                start2 = np.subtract(x, c)
                newD1[start1[0]:start1[0]+self.dicom.dicomSizePixel[0],start1[1]:start1[1]+self.dicom.dicomSizePixel[1],start1[2]:start1[2]+self.dicom.dicomSizePixel[2]]=np.where(self.dicom.dicomData<int(self.spinbox1.value()*2.55), 0, self.dicom.dicomData)
                newD2[start2[0]:start2[0]+self.dicomB.dicomSizePixel[0], start2[1]:start2[1]+self.dicomB.dicomSizePixel[1], start2[2]:start2[2]+self.dicomB.dicomSizePixel[2]] = np.where(self.dicomB.dicomData<int(self.spinbox2.value()*2.55), 0, self.dicomB.dicomData)
                # newD1[start1[2]:start1[2]+self.dicom.dicomSizePixel[2],start1[1]:start1[1]+self.dicom.dicomSizePixel[1],start1[0]:start1[0]+self.dicom.dicomSizePixel[0]]=self.dicom.dicomData
                # newD2[start2[2]:start2[2]+self.dicomB.dicomSizePixel[2], start2[1]:start2[1]+self.dicomB.dicomSizePixel[1], start2[0]:start2[0]+self.dicomB.dicomSizePixel[0]] = self.dicomB.dicomData
                end0=np.maximum(newD1,newD2)


                self.dicomR=DicomClass()
                self.dicomR.dicomData=end0
                self.dicomR.ct1=end0
                self.dicomR.dicomSizePixel=end0.shape
                self.dicomR.scaleM=self.dicom.scaleM
                self.dicomR.scale = self.dicom.scale
                self.dicomR.pos=(10,10,10)
                self.dicomR.zeroPos = (10, 10, 10)
                self.dicomR.dicomSizeMM=np.maximum(self.dicom.dicomSizeMM,self.dicomB.dicomSizeMM)
                dicomRtemp=self.dicomR
                Settings.myList.append(dicomRtemp)
                # self.close()

                self.dicomR.pos = (int(self.dicomR.dicomSizePixel[0] / 2), int(self.dicomR.dicomSizePixel[1] / 2),
                                   int(self.dicomR.dicomSizePixel[2] / 2))
                self.dicomR.zeroPos = (0, 0, 0)
                self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 0)
                self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 1)
                self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 2)

    def sendMain(self):
        if (self.dicomR is not None):
            self.parent.dicomR=self.dicomR
            self.signal.connect(self.parent.receiveCoReg)
            self.signal.emit()






