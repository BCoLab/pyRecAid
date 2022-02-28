# import os,sys
# import dicom as pydicom
# import numpy as np
# from PyQt5 import  QtGui, QtWidgets, QtCore
from contextlib import contextmanager
# import time
# import matplotlib.pyplot as plt
import cv2
# import scipy
import scipy.ndimage
from scipy import ndimage
# import math
from NiftiClass import *
from DicomClass import *
from ResliceForm import *
# from ResliceData import *
# import transforms3d
import Settings
from copy import deepcopy
# from mpl_toolkits import mplot3d
from skimage import measure
import matplotlib.pyplot as plt
from scipy.stats import entropy
import torch
# from sklearn.metrics import mutual_info_score


# from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class CoregistrationForm(QtWidgets.QMainWindow):
    hamed = 83
    dicom = None
    dicomB = None
    dicomR = None
    signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CoregistrationForm, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.points_list = np.zeros((4, 1))
        self.hamed = 1983
        self.pouya = 1996
        self.points_a = []
        self.points_b = []
        self.setGeometry(20, 50, 1700, 920)
        self.setMinimumSize(1710, 980)
        self.setWindowTitle('pyRecAid: Coregistration')
        self.statusBar()

        # list
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.move(50, 50)
        self.listWidget.resize(300, 180)

        # button
        self.openDir = QtWidgets.QPushButton("&Load Folder", self)
        self.openDir.move(67, 250)
        self.openDir.clicked.connect(self.LoadDir)

        # button
        self.loadDataButton = QtWidgets.QPushButton("&Load", self)
        self.loadDataButton.move(233, 250)
        self.loadDataButton.clicked.connect(self.LoadData)
        self.loadDataButton.setEnabled(False)

        # list
        self.listWidgetB = QtWidgets.QListWidget(self)
        self.listWidgetB.move(50, 340)
        self.listWidgetB.resize(300, 180)

        # button
        self.openDirB = QtWidgets.QPushButton("&Load Folder", self)
        self.openDirB.move(67, 540)
        self.openDirB.clicked.connect(self.LoadDirB)

        # button
        self.loadDataButtonB = QtWidgets.QPushButton("&Load", self)
        self.loadDataButtonB.move(233, 540)
        self.loadDataButtonB.clicked.connect(self.LoadDataB)
        self.loadDataButtonB.setEnabled(False)

        # flip region
        self.flipReg = QtWidgets.QGroupBox('&Flip', self)
        self.flipReg.move(67, 685)
        self.flipReg.resize(266, 110)
        self.flipReg.hide()

        # Pouya Box
        self.my_box = QtWidgets.QLabel("Dicom Selection:", self.flipReg)
        self.my_box.move(10, 30)
        self.my_box.resize(150, 30)

        # Pouya list
        self.MRIorCT = QtWidgets.QComboBox(self.flipReg)
        self.MRIorCT.addItem("Select Series")
        self.MRIorCT.addItem("First Series")
        self.MRIorCT.addItem("Second Series")
        self.MRIorCT.move(130, 30)
        self.MRIorCT.resize(130, 30)

        # button pouya
        self.flip_a = QtWidgets.QPushButton("Flip_H", self.flipReg)
        self.flip_a.resize(70, 30)
        self.flip_a.move(10, 70)
        self.flip_a.clicked.connect(self.my_flip_a)

        # button pouya
        self.flip_b = QtWidgets.QPushButton("Flip_S", self.flipReg)
        self.flip_b.resize(70, 30)
        self.flip_b.move(100, 70)
        self.flip_b.clicked.connect(self.my_flip_b)

        # button pouya
        self.flip_c = QtWidgets.QPushButton("Flip_C", self.flipReg)
        self.flip_c.resize(70, 30)
        self.flip_c.move(190, 70)
        self.flip_c.clicked.connect(self.my_flip_c)

        # end of region

        # swap region
        self.swap = QtWidgets.QGroupBox('&Swap', self)
        self.swap.move(67, 805)
        self.swap.resize(266, 110)
        self.swap.hide()

        # Pouya Box
        self.my_box1 = QtWidgets.QLabel("Dicom Selection:", self.swap)
        self.my_box1.move(10, 30)
        self.my_box1.resize(150, 30)

        # Pouya list
        self.MRIorCTs = QtWidgets.QComboBox(self.swap)
        self.MRIorCTs.addItem("Select Series")
        self.MRIorCTs.addItem("First Series")
        self.MRIorCTs.addItem("Second Series")
        self.MRIorCTs.move(130, 30)
        self.MRIorCTs.resize(130, 30)

        # button pouya
        self.swap_a = QtWidgets.QPushButton("Swap12", self.swap)
        self.swap_a.resize(70, 30)
        self.swap_a.move(10, 70)
        self.swap_a.clicked.connect(self.swap12)

        # button pouya
        self.swap_b = QtWidgets.QPushButton("Swap13", self.swap)
        self.swap_b.resize(70, 30)
        self.swap_b.move(100, 70)
        self.swap_b.clicked.connect(self.swap13)

        # button pouya
        self.swap_c = QtWidgets.QPushButton("Swap23", self.swap)
        self.swap_c.resize(70, 30)
        self.swap_c.move(190, 70)
        self.swap_c.clicked.connect(self.swap23)

        # end of region

        # point selection and coregistration region
        self.pointReg = QtWidgets.QGroupBox('&Point selection', self)
        self.pointReg.move(67, 590)
        self.pointReg.resize(266, 90)

        # button pouya
        self.selectpointButton = QtWidgets.QPushButton("&Select Point", self.pointReg)
        self.selectpointButton.resize(100, 30)
        self.selectpointButton.move(15, 55)
        self.selectpointButton.clicked.connect(self.select_point)

        # button pouya
        self.clearpointsButton = QtWidgets.QPushButton("&Clear Points", self.pointReg)
        self.clearpointsButton.resize(100, 30)
        self.clearpointsButton.move(150, 55)
        self.clearpointsButton.clicked.connect(self.clear_point)

        # pouya chekbox
        self.point1 = QtWidgets.QCheckBox('1', self.pointReg)
        self.point1.move(30, 20)
        self.point1.stateChanged.connect(self.checked_box1)

        # pouya chekbox
        self.point2 = QtWidgets.QCheckBox('2', self.pointReg)
        self.point2.move(90, 20)
        self.point2.stateChanged.connect(self.checked_box2)

        # pouya chekbox
        self.point3 = QtWidgets.QCheckBox('3', self.pointReg)
        self.point3.move(150, 20)
        self.point3.stateChanged.connect(self.checked_box3)

        # pouya chekbox
        self.point4 = QtWidgets.QCheckBox('4', self.pointReg)
        self.point4.move(210, 20)
        self.point4.stateChanged.connect(self.checked_box4)

        # end of region

        # button
        self.combineButton = QtWidgets.QPushButton("&Coregistration", self)
        self.combineButton.resize(140, 30)
        self.combineButton.move(50, 940)
        self.combineButton.clicked.connect(self.combine)

        # button
        self.sendMainButton = QtWidgets.QPushButton("&Send To MainForm", self)
        self.sendMainButton.resize(140, 30)
        self.sendMainButton.move(210, 940)
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
        self.img0.wheelEvent = self.wheelEventImg0Event
        self.img0.mouseDoubleClickEvent = self.DoubleClickEventImg0Event
        self.img0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImg0 = QtWidgets.QLabel("", self)
        self.labelImg0.move(402, 52)
        self.labelImg0.resize(350, 18)
        self.labelImg0.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg0.setFont(font)

        self.column_title0 = QtWidgets.QLabel("Horizontal", self)
        self.column_title0.move(560, 20)
        self.column_title0.resize(350, 30)
        self.column_title0.setStyleSheet('QLabel {color: #888888;}')
        self.column_title0.setFont(font)

        self.row_title0 = QtWidgets.QLabel("1st", self)
        self.row_title0.move(370, 175)
        self.row_title0.resize(350, 30)
        self.row_title0.setStyleSheet('QLabel {color: #000000;}')
        self.row_title0.setFont(font)

        # img1
        self.img1 = QtWidgets.QLabel(self)
        self.img1.move(830, 50)
        self.img1.resize(420, 280)
        self.img1.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap2 = QtGui.QPixmap("dicom.png")
        self.img1.setPixmap(pixmap2)
        self.img1.setScaledContents(1)
        self.img1.wheelEvent = self.wheelEventImg1Event
        self.img1.mouseDoubleClickEvent = self.DoubleClickEventImg1Event
        self.img1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImg1 = QtWidgets.QLabel("", self)
        self.labelImg1.move(832, 52)
        self.labelImg1.resize(350, 18)
        self.labelImg1.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg1.setFont(font)

        self.column_title1 = QtWidgets.QLabel("Sagittal", self)
        self.column_title1.move(1010, 20)
        self.column_title1.resize(350, 30)
        self.column_title1.setStyleSheet('QLabel {color: #888888;}')
        self.column_title1.setFont(font)

        self.row_title1 = QtWidgets.QLabel("2nd", self)
        self.row_title1.move(365, 465)
        self.row_title1.resize(350, 30)
        self.row_title1.setStyleSheet('QLabel {color: #000000;}')
        self.row_title1.setFont(font)

        # img2
        self.img2 = QtWidgets.QLabel(self)
        self.img2.move(1260, 50)
        self.img2.resize(420, 280)
        self.img2.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap3 = QtGui.QPixmap("dicom.png")
        self.img2.setPixmap(pixmap3)
        self.img2.setScaledContents(1)
        self.img2.wheelEvent = self.wheelEventImg2Event
        self.img2.mouseDoubleClickEvent = self.DoubleClickEventImg2Event
        self.img2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImg2 = QtWidgets.QLabel("", self)
        self.labelImg2.move(1262, 52)
        self.labelImg2.resize(350, 18)
        self.labelImg2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg2.setFont(font)

        self.column_title2 = QtWidgets.QLabel("Coronal", self)
        self.column_title2.move(1435, 20)
        self.column_title2.resize(350, 30)
        self.column_title2.setStyleSheet('QLabel {color: #888888;}')
        self.column_title2.setFont(font)

        self.row_title2 = QtWidgets.QLabel("Cr", self)
        self.row_title2.move(377, 755)
        self.row_title2.resize(350, 30)
        self.row_title2.setStyleSheet('QLabel {color: #000000;}')
        self.row_title2.setFont(font)

        # imgb0
        self.imgb0 = QtWidgets.QLabel(self)
        self.imgb0.move(400, 340)
        self.imgb0.resize(420, 280)
        self.imgb0.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap = QtGui.QPixmap("dicom.png")
        self.imgb0.setPixmap(pixmap)
        self.imgb0.setScaledContents(1)
        self.imgb0.wheelEvent = self.wheelEventImgb0Event
        self.imgb0.mouseDoubleClickEvent = self.DoubleClickEventImgb0Event
        self.imgb0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImgb0 = QtWidgets.QLabel("", self)
        self.labelImgb0.move(402, 342)
        self.labelImgb0.resize(350, 18)
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
        self.imgb1.mouseDoubleClickEvent = self.DoubleClickEventImgb1Event
        self.imgb1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgb1 = QtWidgets.QLabel("", self)
        self.labelImgb1.move(832, 342)
        self.labelImgb1.resize(350, 18)
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
        self.imgb2.mouseDoubleClickEvent = self.DoubleClickEventImgb2Event
        self.imgb2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgb2 = QtWidgets.QLabel("", self)
        self.labelImgb2.move(1262, 342)
        self.labelImgb2.resize(350, 18)
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
        self.imgc0.wheelEvent = self.wheelEventImgc0Event
        self.imgc0.mouseDoubleClickEvent = self.DoubleClickEventImgc0Event
        self.imgc0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImgc0 = QtWidgets.QLabel("", self)
        self.labelImgc0.move(402, 632)
        self.labelImgc0.resize(350, 18)
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
        self.imgc1.mouseDoubleClickEvent = self.DoubleClickEventImgc1Event
        self.imgc1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgc1 = QtWidgets.QLabel("", self)
        self.labelImgc1.move(832, 632)
        self.labelImgc1.resize(350, 18)
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
        self.imgc2.mouseDoubleClickEvent = self.DoubleClickEventImgc2Event
        self.imgc2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImgc2 = QtWidgets.QLabel("", self)
        self.labelImgc2.move(1262, 632)
        self.labelImgc2.resize(350, 18)
        self.labelImgc2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImgc2.setFont(font)

        # region ReSlice
        # group box
        # self.groupBox = QtWidgets.QGroupBox('&Impact option', self)
        # self.groupBox.move(67, 670)
        # self.groupBox.resize(266, 60)

        # spinbox
        # self.spinboxLabel0 = QtWidgets.QLabel("X:", self.groupBox)
        # self.spinboxLabel0.move(20, 25)
        # self.spinbox0 = QtWidgets.QSpinBox(self.groupBox)
        # self.spinbox0.move(40, 25)
        # self.spinbox0.setMinimum(-180)
        # self.spinbox0.setMaximum(180)
        # self.spinbox0.setValue(0)

        # self.spinboxLabel1 = QtWidgets.QLabel("Image 1:", self.groupBox)
        # self.spinboxLabel1.move(5, 25)
        # self.spinbox1 = QtWidgets.QSpinBox(self.groupBox)
        # self.spinbox1.move(55, 23)
        # self.spinbox1.setMinimum(0)
        # self.spinbox1.setMaximum(100)
        # self.spinbox1.setValue(0)
        #
        # self.spinboxLabel2 = QtWidgets.QLabel("Image 2:", self.groupBox)
        # self.spinboxLabel2.move(130, 25)
        # self.spinbox2 = QtWidgets.QSpinBox(self.groupBox)
        # self.spinbox2.move(190, 23)
        # self.spinbox2.setMinimum(0)
        # self.spinbox2.setMaximum(100)
        # self.spinbox2.setValue(0)

        flipMenu = QtWidgets.QAction('Flip', self)
        flipMenu.setCheckable(True)
        flipMenu.setStatusTip('flip')
        flipMenu.triggered.connect(self.FlipMenu)

        swapMenu = QtWidgets.QAction('Swap', self)
        swapMenu.setCheckable(True)
        swapMenu.setStatusTip('swap')
        swapMenu.triggered.connect(self.SwapMenu)


        # menu
        openFile = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.LoadDir)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        toolsMenu = menubar.addMenu('&Tools')
        fileMenu.addAction(openFile)
        toolsMenu.addAction(flipMenu)
        toolsMenu.addAction(swapMenu)

        self.Fflag = False
        self.Sflag = False

    def FlipMenu(self):
        if self.Fflag:
            self.flipReg.hide()
            self.Fflag = False
        else:
            self.flipReg.show()
            self.Fflag = True

    def SwapMenu(self):
        if self.Sflag:
            self.swap.hide()
            self.Sflag = False
        else:
            self.swap.show()
            self.Sflag = True

    @contextmanager
    def WaitCursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def LoadDir(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        try:
            with self.WaitCursor():
                if fname[0]:
                    self.listWidget.clear()
                    self.dicom = DicomClass()
                    xx = self.dicom.DicomSelect(fname)
                    for i in range(len(xx)):
                        item = QtWidgets.QListWidgetItem(xx[i])
                        self.listWidget.addItem(item)
                if (~self.loadDataButton.isEnabled()):
                    self.loadDataButton.setEnabled(True)
                # self.mainform.dicom = []
        except:
            # time.sleep(0.001)
            with self.WaitCursor():
                if fname[0]:
                    self.listWidget.clear()
                    self.dicom = NiftiClass()
                    xx = self.dicom.DicomSelect(fname)
                    for i in range(len(xx)):
                        item = QtWidgets.QListWidgetItem(xx[i])
                        self.listWidget.addItem(item)
                if (~self.loadDataButton.isEnabled()):
                    self.loadDataButton.setEnabled(True)
                # self.mainform.dicom = []

    def LoadDirB(self):
        print('ok1')
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        try:
            with self.WaitCursor():
                if fname[0]:
                    self.listWidgetB.clear()
                    self.dicomB = DicomClass()
                    xx = self.dicomB.DicomSelect(fname)
                    for i in range(len(xx)):
                        item = QtWidgets.QListWidgetItem(xx[i])
                        self.listWidgetB.addItem(item)
                if (~self.loadDataButtonB.isEnabled()):
                    self.loadDataButtonB.setEnabled(True)
        except:
            with self.WaitCursor():
                if fname[0]:
                    self.listWidgetB.clear()
                    self.dicomB = NiftiClass()
                    xx = self.dicomB.DicomSelect(fname)
                    for i in range(len(xx)):
                        item = QtWidgets.QListWidgetItem(xx[i])
                        self.listWidgetB.addItem(item)
                if (~self.loadDataButtonB.isEnabled()):
                    self.loadDataButtonB.setEnabled(True)

    def LoadData(self):
        try:
            value = int(self.listWidget.currentItem().text()[0:2])
            with self.WaitCursor():
                self.dicom.DicomRead(value, 1)
                # self.dicom.dicomSize=np.shape(self.dicom.dicomData)
                self.dicom.pos = (int(self.dicom.dicomSizePixel[0] / 2), int(self.dicom.dicomSizePixel[1] / 2),
                                  int(self.dicom.dicomSizePixel[2] / 2))
                self.dicom.zeroPos = (0, 0, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

        except:
            value = self.listWidget.currentItem().text()
            with self.WaitCursor():
                self.dicom.DicomRead(value)

                # for i in range(self.dicom.dicomSizePixel[0]):
                #     self.dicom.dicomData[i, :, :] = np.flip(self.dicom.dicomData[i, :, :], axis=1)
                # self.dicom.dicomDataRaw = copy.deepcopy(self.dicom.dicomData)

                self.dicom.pos = (int(self.dicom.dicomSizePixel[0] / 2), int(self.dicom.dicomSizePixel[1] / 2),
                                  int(self.dicom.dicomSizePixel[2] / 2))
                self.dicom.zeroPos = (0, 0, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

        #     msg = QtWidgets.QMessageBox()
        #     msg.setIcon(QtWidgets.QMessageBox.Information)
        #     msg.setWindowTitle("Error")
        #     msg.setText('Dicom Series is not correct')
        #     msg.exec_()

    def LoadDataB(self):
        try:
            value = int(self.listWidgetB.currentItem().text()[0:2])
            with self.WaitCursor():
                self.dicomB.DicomRead(value, 1)

                # self.dicomB.dicomSize=np.shape(self.dicomB.dicomData)
                self.dicomB.pos = (int(self.dicomB.dicomSizePixel[0] / 2), int(self.dicomB.dicomSizePixel[1] / 2),
                                   int(self.dicomB.dicomSizePixel[2] / 2))
                self.dicomB.zeroPos = (0, 0, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

        except:
            value = self.listWidget.currentItem().text()
            with self.WaitCursor():
                self.dicomB.DicomRead(value)

                self.dicomB.pos = (int(self.dicomB.dicomSizePixel[0] / 2), int(self.dicomB.dicomSizePixel[1] / 2),
                                  int(self.dicomB.dicomSizePixel[2] / 2))
                self.dicomB.zeroPos = (0, 0, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)
            # msg = QtWidgets.QMessageBox()
            # msg.setIcon(QtWidgets.QMessageBox.Information)
            # msg.setWindowTitle("Error")
            # msg.setText('Dicom Series is not correct')
            # msg.exec_()

    def ShowDicom(self, ct, pos, frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        # plt.hist(a0, bins=256)
        # plt.show()


        pix0 = self.CreateQPixmap(a0, round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]),
                                  round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]), pos[2], pos[1],
                                  self.dicom.markerPos[2], self.dicom.markerPos[1], 2, 1, self.dicom.markerFlag)
        pix1 = self.CreateQPixmap(a1, round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                  round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]), pos[0], pos[2],
                                  self.dicom.markerPos[0], self.dicom.markerPos[2], 0, 2, self.dicom.markerFlag)
        pix2 = self.CreateQPixmap(a2, round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                  round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]), pos[0], pos[1],
                                  self.dicom.markerPos[0], self.dicom.markerPos[1], 0, 1, self.dicom.markerFlag)
        self.img0.setPixmap(pix0)
        self.img0.setScaledContents(1)
        self.img1.setPixmap(pix1)
        self.img1.setScaledContents(1)
        self.img2.setPixmap(pix2)
        self.img2.setScaledContents(1)
        if frame == 0:
            self.labelImg0.setText(str(round((pos[0] - self.dicom.zeroPos[0]) * self.dicom.scaleM[0], 2)) + "mm")
        if frame == 1:
            self.labelImg1.setText(str(round((pos[1] - self.dicom.zeroPos[1]) * self.dicom.scaleM[1], 2)) + "mm")
        if frame == 2:
            self.labelImg2.setText(str(round((pos[2] - self.dicom.zeroPos[2]) * self.dicom.scaleM[2], 2)) + "mm")

    def ShowDicomB(self, ct, pos, frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        # plt.hist(a0, bins=256)
        # plt.show()


        pix0 = self.CreateQPixmap(a0, round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]),
                                  round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]), pos[2], pos[1],
                                  self.dicomB.markerPos[2], self.dicomB.markerPos[1], 2, 1, self.dicomB.markerFlag)
        pix1 = self.CreateQPixmap(a1, round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0]),
                                  round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]), pos[0], pos[2],
                                  self.dicomB.markerPos[0], self.dicomB.markerPos[2], 0, 2, self.dicomB.markerFlag)
        pix2 = self.CreateQPixmap(a2, round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0]),
                                  round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]), pos[0], pos[1],
                                  self.dicomB.markerPos[0], self.dicomB.markerPos[1], 0, 1, self.dicomB.markerFlag)
        self.imgb0.setPixmap(pix0)
        self.imgb0.setScaledContents(1)
        self.imgb1.setPixmap(pix1)
        self.imgb1.setScaledContents(1)
        self.imgb2.setPixmap(pix2)
        self.imgb2.setScaledContents(1)
        if frame == 0:
            self.labelImgb0.setText(str(round((pos[0] - self.dicomB.zeroPos[0]) * self.dicomB.scaleM[0], 2)) + "mm")
        if frame == 1:
            self.labelImgb1.setText(str(round((pos[1] - self.dicomB.zeroPos[1]) * self.dicomB.scaleM[1], 2)) + "mm")
        if frame == 2:
            self.labelImgb2.setText(str(round((pos[2] - self.dicomB.zeroPos[2]) * self.dicomB.scaleM[2], 2)) + "mm")

    def ShowDicomR(self, ct, pos, frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]


        # a0 = cv2.resize(a0, np.shape(a0), interpolation=cv2.INTER_AREA)
        # a1 = cv2.resize(a1, np.shape(a1), interpolation=cv2.INTER_AREA)
        # a2 = cv2.resize(a2, np.shape(a2), interpolation=cv2.INTER_AREA)



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
            self.labelImgc0.setText(str(round((pos[0] - self.dicomR.zeroPos[0]) * self.dicomR.scaleM[0], 2)) + "mm")
        if frame == 1:
            self.labelImgc1.setText(str(round((pos[1] - self.dicomR.zeroPos[1]) * self.dicomR.scaleM[1], 2)) + "mm")
        if frame == 2:
            self.labelImgc2.setText(str(round((pos[2] - self.dicomR.zeroPos[2]) * self.dicomR.scaleM[2], 2)) + "mm")

    def CreateQPixmap(self, data, scl0, scl1, x1, y1, x2, y2, color1, color2, markerFlag):
        b = np.zeros((np.shape(data)[0], np.shape(data)[1], 3), dtype=np.uint8)
        b[:, :, 0] = data
        b[:, :, 1] = data
        b[:, :, 2] = data
        b[x1, :, color1] = 255
        b[:, y1, color2] = 255

        color3 = 3 - (color1 + color2)
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

    def wheelEventImg0Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicom.pos[0] < self.dicom.dicomSizePixel[0] - 1):
                        self.dicom.pos = (self.dicom.pos[0] + 1, self.dicom.pos[1], self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[0] > 0):
                        self.dicom.pos = (self.dicom.pos[0] - 1, self.dicom.pos[1], self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 0)

    def wheelEventImg1Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicom.pos[1] < self.dicom.dicomSizePixel[1] - 1):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1] + 1, self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[1] > 0):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1] - 1, self.dicom.pos[2])
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 1)

    def wheelEventImg2Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicom.pos[2] < self.dicom.dicomSizePixel[2] - 1):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1], self.dicom.pos[2] + 1)
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[2] > 0):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1], self.dicom.pos[2] - 1)
                        self.ShowDicom(self.dicom.ct1, self.dicom.pos, 2)

    def DoubleClickEventImg0Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a0 = np.transpose(self.dicom.dicomData[self.dicom.pos[0], :, :], (1, 0))
                a0 = cv2.resize(a0, (int(round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1])),
                                     int(round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]))),
                                interpolation=cv2.INTER_AREA)

                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg1Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a1 = np.transpose(self.dicom.dicomData[:, self.dicom.pos[1], :], (0, 1))
                a1 = cv2.resize(a1, (int(round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0])),
                                     int(round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]))),
                                interpolation=cv2.INTER_AREA)

                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg2Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a2 = self.dicom.dicomData[:, :, self.dicom.pos[2]]
                a2 = cv2.resize(a2, (int(round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0])),
                                     int(round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]))),
                                interpolation=cv2.INTER_AREA)

                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def wheelEventImgb0Event(self, event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicomB.pos[0] < self.dicomB.dicomSizePixel[0] - 1):
                        self.dicomB.pos = (self.dicomB.pos[0] + 1, self.dicomB.pos[1], self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicomB.pos[0] > 0):
                        self.dicomB.pos = (self.dicomB.pos[0] - 1, self.dicomB.pos[1], self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 0)

    def wheelEventImgb1Event(self, event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicomB.pos[1] < self.dicomB.dicomSizePixel[1] - 1):
                        self.dicomB.pos = (self.dicomB.pos[0], self.dicomB.pos[1] + 1, self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicomB.pos[1] > 0):
                        self.dicomB.pos = (self.dicomB.pos[0], self.dicomB.pos[1] - 1, self.dicomB.pos[2])
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 1)

    def wheelEventImgb2Event(self, event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicomB.pos[2] < self.dicomB.dicomSizePixel[2] - 1):
                        self.dicomB.pos = (self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2] + 1)
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicomB.pos[2] > 0):
                        self.dicomB.pos = (self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2] - 1)
                        self.ShowDicomB(self.dicomB.ct1, self.dicomB.pos, 2)

    def DoubleClickEventImgb0Event(self, event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                a0 = np.transpose(self.dicomB.dicomData[self.dicomB.pos[0], :, :], (1, 0))
                a0 = cv2.resize(a0, (int(round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1])),
                                     int(round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]))),
                                interpolation=cv2.INTER_AREA)

                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgb1Event(self, event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                a1 = np.transpose(self.dicomB.dicomData[:, self.dicomB.pos[1], :], (0, 1))
                a1 = cv2.resize(a1, (int(round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0])),
                                     int(round(self.dicomB.scale[2] * self.dicomB.dicomSizePixel[2]))),
                                interpolation=cv2.INTER_AREA)

                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgb2Event(self, event):
        if self.dicomB is not None:
            if self.dicomB.dicomData != []:
                a2 = self.dicomB.dicomData[:, :, self.dicomB.pos[2]]
                a2 = cv2.resize(a2, (int(round(self.dicomB.scale[0] * self.dicomB.dicomSizePixel[0])),
                                     int(round(self.dicomB.scale[1] * self.dicomB.dicomSizePixel[1]))),
                                interpolation=cv2.INTER_AREA)

                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def wheelEventImgc0Event(self, event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicomR.pos[0] < self.dicomR.dicomSizePixel[0] - 1):
                        self.dicomR.pos = (self.dicomR.pos[0] + 1, self.dicomR.pos[1], self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicomR.pos[0] > 0):
                        self.dicomR.pos = (self.dicomR.pos[0] - 1, self.dicomR.pos[1], self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 0)

    def wheelEventImgc1Event(self, event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicomR.pos[1] < self.dicomR.dicomSizePixel[1] - 1):
                        self.dicomR.pos = (self.dicomR.pos[0], self.dicomR.pos[1] + 1, self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicomR.pos[1] > 0):
                        self.dicomR.pos = (self.dicomR.pos[0], self.dicomR.pos[1] - 1, self.dicomR.pos[2])
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 1)

    def wheelEventImgc2Event(self, event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicomR.pos[2] < self.dicomR.dicomSizePixel[2] - 1):
                        self.dicomR.pos = (self.dicomR.pos[0], self.dicomR.pos[1], self.dicomR.pos[2] + 1)
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicomR.pos[2] > 0):
                        self.dicomR.pos = (self.dicomR.pos[0], self.dicomR.pos[1], self.dicomR.pos[2] - 1)
                        self.ShowDicomR(self.dicomR.ct1, self.dicomR.pos, 2)

    def DoubleClickEventImgc0Event(self, event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                a0 = np.transpose(self.dicomR.dicomData[self.dicomR.pos[0], :, :], (1, 0))
                a0 = cv2.resize(a0, (int(round(self.dicomR.scale[1] * self.dicomR.dicomSizePixel[1])),
                                     int(round(self.dicomR.scale[2] * self.dicomR.dicomSizePixel[2]))),
                                interpolation=cv2.INTER_AREA)
                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgc1Event(self, event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                a1 = np.transpose(self.dicomR.dicomData[:, self.dicomR.pos[1], :], (0, 1))
                a1 = cv2.resize(a1, (int(round(self.dicomR.scale[0] * self.dicomR.dicomSizePixel[0])),
                                     int(round(self.dicomR.scale[2] * self.dicomR.dicomSizePixel[2]))),
                                interpolation=cv2.INTER_AREA)
                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImgc2Event(self, event):
        if self.dicomR is not None:
            if self.dicomR.dicomData != []:
                a2 = self.dicomR.dicomData[:, :, self.dicomR.pos[2]]
                a2 = cv2.resize(a2, (int(round(self.dicomR.scale[0] * self.dicomR.dicomSizePixel[0])),
                                     int(round(self.dicomR.scale[1] * self.dicomR.dicomSizePixel[1]))),
                                interpolation=cv2.INTER_AREA)
                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def swap12(self):
        if self.MRIorCTs.currentIndex() == 1:
            if self.dicom is not None:
                self.dicom.dicomData = np.transpose(self.dicom.dicomData, (1, 0, 2))
                self.dicom.ct1 = np.transpose(self.dicom.ct1, (1, 0, 2))
                self.dicom.dicomSizePixel = np.shape(self.dicom.dicomData)
                self.dicom.pos = (int(self.dicom.dicomSizePixel[0] / 2), int(self.dicom.dicomSizePixel[1] / 2),
                                   int(self.dicom.dicomSizePixel[2] / 2))
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
        if self.MRIorCTs.currentIndex() == 2:
            if self.dicomB is not None:
                print('ok')
                self.dicomB.dicomData = np.transpose(self.dicomB.dicomData, (1, 0, 2))
                self.dicomB.ct1 = np.transpose(self.dicomB.ct1, (1, 0, 2))
                self.dicomB.dicomSizePixel = np.shape(self.dicomB.dicomData)
                self.dicomB.pos = (int(self.dicomB.dicomSizePixel[0] / 2), int(self.dicomB.dicomSizePixel[1] / 2),
                                   int(self.dicomB.dicomSizePixel[2] / 2))
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

    def swap13(self):
        if self.MRIorCTs.currentIndex() == 1:
            if self.dicom is not None:
                self.dicom.dicomData = np.transpose(self.dicom.dicomData, (2, 1, 0))
                self.dicom.ct1 = np.transpose(self.dicom.ct1, (2, 1, 0))
                self.dicom.dicomSizePixel = np.shape(self.dicom.dicomData)
                self.dicom.pos = (int(self.dicom.dicomSizePixel[0] / 2), int(self.dicom.dicomSizePixel[1] / 2),
                                  int(self.dicom.dicomSizePixel[2] / 2))
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
        if self.MRIorCTs.currentIndex() == 2:
            if self.dicomB is not None:
                self.dicomB.dicomData = np.transpose(self.dicomB.dicomData, (2, 1, 0))
                self.dicomB.ct1 = np.transpose(self.dicomB.ct1, (2, 1, 0))
                self.dicomB.dicomSizePixel = np.shape(self.dicomB.dicomData)
                self.dicomB.pos = (int(self.dicomB.dicomSizePixel[0] / 2), int(self.dicomB.dicomSizePixel[1] / 2),
                                   int(self.dicomB.dicomSizePixel[2] / 2))
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

    def swap23(self):
        if self.MRIorCTs.currentIndex() == 1:
            if self.dicom is not None:
                self.dicom.dicomData = np.transpose(self.dicom.dicomData, (0, 2, 1))
                self.dicom.ct1 = np.transpose(self.dicom.ct1, (0, 2, 1))
                self.dicom.dicomSizePixel = np.shape(self.dicom.dicomData)
                self.dicom.pos = (int(self.dicom.dicomSizePixel[0] / 2), int(self.dicom.dicomSizePixel[1] / 2),
                                  int(self.dicom.dicomSizePixel[2] / 2))
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
        if self.MRIorCTs.currentIndex() == 2:
            if self.dicomB is not None:
                self.dicomB.dicomData = np.transpose(self.dicomB.dicomData, (0, 2, 1))
                self.dicomB.ct1 = np.transpose(self.dicomB.ct1, (0, 2, 1))
                self.dicomB.dicomSizePixel = np.shape(self.dicomB.dicomData)
                self.dicomB.pos = (int(self.dicomB.dicomSizePixel[0] / 2), int(self.dicomB.dicomSizePixel[1] / 2),
                                  int(self.dicomB.dicomSizePixel[2] / 2))
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

    def my_flip_a(self):
        if self.MRIorCT.currentIndex() == 1:
            if self.dicom is not None:
                for i in range(self.dicom.dicomSizePixel[0]):
                    self.dicom.dicomData[i, :, :] = np.flip(self.dicom.dicomData[i, :, :], axis=1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
        elif self.MRIorCT.currentIndex() == 2:
            if self.dicomB is not None:
                for i in range(self.dicomB.dicomSizePixel[0]):
                    self.dicomB.dicomData[i, :, :] = np.flip(self.dicomB.dicomData[i, :, :], axis=1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

    def my_flip_b(self):
        if self.MRIorCT.currentIndex() == 1:
            if self.dicom is not None:
                for i in range(self.dicom.dicomSizePixel[1]):
                    self.dicom.dicomData[:, i, :] = np.flip(self.dicom.dicomData[:, i, :], axis=1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
        elif self.MRIorCT.currentIndex() == 2:
            if self.dicomB is not None:
                for i in range(self.dicomB.dicomSizePixel[1]):
                    self.dicomB.dicomData[:, i, :] = np.flip(self.dicomB.dicomData[:, i, :], axis=1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

    def my_flip_c(self):
        if self.MRIorCT.currentIndex() == 1:
            if self.dicom is not None:
                for i in range(self.dicom.dicomSizePixel[2]):
                    self.dicom.dicomData[:, :, i] = np.flip(self.dicom.dicomData[:, :, i], axis=0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
        if self.MRIorCT.currentIndex() == 2:
            if self.dicomB is not None:
                for i in range(self.dicomB.dicomSizePixel[2]):
                    self.dicomB.dicomData[:, :, i] = np.flip(self.dicomB.dicomData[:, :, i], axis=0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 0)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 1)
                self.ShowDicomB(self.dicomB.dicomData, self.dicomB.pos, 2)

    def checked_box1(self):
        if (self.dicom is not None) and (self.dicomB is not None):
            if (sum(self.points_list) != 0) and (sum(self.points_list) < 5):
                if not (self.point1.isChecked()):
                    self.points_a.pop(0)
                    self.points_b.pop(0)
                    # self.cnt -= 1
                    self.points_list[0] = 0

    def checked_box2(self):
        if (self.dicom is not None) and (self.dicomB is not None):
            if (sum(self.points_list) != 0) and (sum(self.points_list) < 5):
                if not (self.point2.isChecked()):
                    self.points_a.pop(1)
                    self.points_b.pop(1)
                    # self.cnt -= 1
                    self.points_list[1] = 0

    def checked_box3(self):
        if (self.dicom is not None) and (self.dicomB is not None):
            if (sum(self.points_list) != 0) and (sum(self.points_list) < 5):
                if not (self.point3.isChecked()):
                    self.points_a.pop(2)
                    self.points_b.pop(2)
                    # self.cnt -= 1
                    self.points_list[2] = 0

    def checked_box4(self):
        if (self.dicom is not None) and (self.dicomB is not None):
            if (sum(self.points_list) != 0) and (sum(self.points_list) < 5):
                if not (self.point4.isChecked()):
                    self.points_a.pop(3)
                    self.points_b.pop(3)
                    # self.cnt -= 1
                    self.points_list[3] = 0

    def select_point(self):
        if (self.dicom is not None) and (self.dicomB is not None):
            # self.cnt += 1
            # self.points_a.append(self.dicom.pos)
            # self.points_b.append((self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2]))
            if self.points_list[0] == 0:
                # if not(self.point1.isChecked()):
                self.point1.setChecked(True)
                self.points_list[0] = 1
                self.points_a.insert(0, self.dicom.pos)
                self.points_b.insert(0, (self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2]))
            elif self.points_list[1] == 0:
                self.point2.setChecked(True)
                self.points_list[1] = 1
                self.points_a.insert(1, self.dicom.pos)
                self.points_b.insert(1, (self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2]))
            elif self.points_list[2] == 0:
                self.point3.setChecked(True)
                self.points_list[2] = 1
                self.points_a.insert(2, self.dicom.pos)
                self.points_b.insert(2, (self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2]))
            elif self.points_list[3] == 0:
                self.point4.setChecked(True)
                self.points_list[3] = 1
                self.points_a.insert(3, self.dicom.pos)
                self.points_b.insert(3, (self.dicomB.pos[0], self.dicomB.pos[1], self.dicomB.pos[2]))
            else:
                warning = QtWidgets.QMessageBox.question(self, 'Warning',
                                                         "You have selected enough points!",
                                                         QtWidgets.QMessageBox.Ok)
                if warning == QtWidgets.QMessageBox.Ok:
                    pass

        # konani
        # [(51, 109, 102), (51, 46, 108), (190, 74, 94), (146, 78, 215)]
        # [(19, 152, 141), (15, 90, 132), (153, 112, 139), (94, 111, 368)]

        # Giyasvand (176, 472)
        # [(77, 133, 94), (82, 57, 92), (202, 102, 26), (201, 102, 145)]
        # [(74, 196, 453), (69, 127, 458), (201, 150, 483), (121, 161, 667)]

        # Bonyad mir azm
        # [(153, 98, 190), (153, 93, 63), (69, 135, 106), (69, 58, 108)]
        # [(156, 121, 380), (156, 107, 146), (72, 156, 190), (72, 85, 205)]

    def clear_point(self):
        self.points_list = np.zeros((4, 1))
        self.point1.setChecked(False)
        self.point2.setChecked(False)
        self.point3.setChecked(False)
        self.point4.setChecked(False)
        self.points_a.clear()
        self.points_b.clear()            

    def combine(self):
        if ((self.dicom is not None) and (self.dicomB is not None)):
            with self.WaitCursor():
                # print(self.points_a)
                # print(self.points_b)

                self.points_a = [(24, 74, 141), (91, 76, 206), (96, 12, 87), (93, 137, 84)]
                self.points_b = [(81, 110, 236), (154, 110, 358), (139, 53, 104), (132, 175, 120)]

                # self.points_a = [(153, 98, 190), (153, 93, 63), (69, 135, 106), (69, 58, 108)]
                # self.points_b = [(156, 121, 380), (156, 107, 146), (72, 156, 190), (72, 85, 205)]

                if len(self.points_a) < 4:
                    warning = QtWidgets.QMessageBox.question(self, 'Warning',
                                                             "You have not selected enough points!",
                                                             QtWidgets.QMessageBox.Ok)
                    if warning == QtWidgets.QMessageBox.Ok:
                        pass
                
                else:
                    _, M, _ = cv2.estimateAffine3D(np.float32(self.points_a), np.float32(self.points_b))

                    # print(M)
                    # print(self.points_a)
                    # print(self.points_b)

                    pouya = ndimage.affine_transform(self.dicomB.dicomData, M, output_shape=self.dicom.dicomSizePixel)

                    # pouya = cv2.resize(pouya, (int(round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1])),
                    #                    int(round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]))),
                    #                    interpolation=cv2.INTER_AREA)

                    # xxx = self.voxel_selection(pouya, self.dicom.dicomData)
                    # print(xxx)

                    # print(np.shape(np.where(self.dicom.dicomData>200)[0]))
                    # print(np.where(self.dicom.dicomData>200)[0])
                    # pouya = np.maximum(pouya, self.dicom.dicomData)

                    # shape = np.shape(pouya)
                    # print(plt.hist(pouya[shape[0]//2][shape[1]//2][shape[2]//2].reshape((-1, 1)), density=True, bins=256))
                    # plt.show()

                    ######################################################################################################
                    # shape = np.shape(pouya)
                    # pp1 = np.reshape(pouya, (-1))
                    # pp2 = np.reshape(self.dicom.dicomData, (-1))

                    # import time
                    # tic = time.time()
                    # pp1 = ndimage.generic_filter(pp1, np.var, size=5)
                    # pp2 = ndimage.generic_filter(pp2, np.var, size=5)

                    # pp1 = np.reshape(pp1, shape)
                    # pp2 = np.reshape(pp2, shape)
                    # print(time.time()-tic)
                    ######################################################################################################
                    with torch.no_grad():
                        KS = 11
                        pad = KS//2
                        m = torch.nn.Conv3d(1,1,KS, stride=2, padding=pad)
                        m.weight.data.fill_(1)
                        m.bias.data.fill_(1)

                        pp1 = torch.unsqueeze(torch.unsqueeze(torch.FloatTensor(np.power(pouya,2)), 0), 0)
                        pp2 = torch.unsqueeze(torch.unsqueeze(torch.FloatTensor(np.power(self.dicom.dicomData,2)), 0), 0)

                        pp1 = m(pp1)/KS
                        pp1_m = m(torch.unsqueeze(torch.unsqueeze(torch.FloatTensor(pouya), 0), 0))/KS
                        ##################################################################################################
                        pp2 = m(pp2)/KS
                        pp2_m = m(torch.unsqueeze(torch.unsqueeze(torch.FloatTensor(self.dicom.dicomData), 0), 0))/KS

                    pp1 = pp1 - pp1_m
                    pp2 = pp2 - pp2_m

                    # print(pp1.shape)
                    # print(pp2.shape)
                    # print('########################')

                    mm = torch.nn.Upsample(size=np.shape(pouya), mode='nearest')
                    pp1 = mm(pp1).numpy()[0][0]
                    pp2 = mm(pp2).numpy()[0][0]

                    # print(np.shape(pp1))
                    # print(np.shape(pp2))
                    # print('########################')


                    # print('ok1')
                    # pp1 = ndimage.generic_filter(pp1, np.mean, size=(3,3,3))
                    # pp2 = ndimage.generic_filter(self.dicom.dicomData, np.mean, size=(3,3,3))
                    ######################################################################################################
                    # import time
                    # pp1 = np.zeros_like(pouya)
                    # pp2 = np.zeros_like(pouya)

                    # print('##################################################################')
                    # print(len(pouya))
                    
                    # tic = time.time()
                    # for i in range(np.shape(pouya)[2]//2, np.shape(pouya)[2]):
                    #     pp1[:,:,i] = ndimage.generic_filter(pouya[:,:,i], np.var, size=(3,3))
                    #     pp2[:,:,i] = ndimage.generic_filter(self.dicom.dicomData[:,:,i], np.var, size=(3,3))

                    # print('ok')
                    # print(time.time()-tic)
                    # print('##################################################################')
                    ######################################################################################################

                    # pouya = np.where(pouya-80>self.dicom.dicomData, pouya, self.dicom.dicomData)
                    pouya = np.where(pp1<pp2, pouya, self.dicom.dicomData)


                    self.dicomR = DicomClass()
                    self.dicomR.dicomData = pouya  #
                    self.dicomR.ct1 = pouya  #
                    self.dicomR.dicomSizePixel = pouya.shape  #
                    self.dicomR.scaleM = self.dicom.scaleM
                    self.dicomR.scale = self.dicom.scale
                    self.dicomR.pos = (10, 10, 10)
                    self.dicomR.zeroPos = (0, 0, 0)
                    # self.dicomR.dicomSizeMM = np.maximum(self.dicom.dicomSizeMM,self.dicomB.dicomSizeMM)
                    self.dicomR.dicomSizeMM = pouya.shape  #
                    dicomRtemp = self.dicomR
                    Settings.myList.append(dicomRtemp)

                    self.dicomR.pos = (int(self.dicomR.dicomSizePixel[0] / 2), int(self.dicomR.dicomSizePixel[1] / 2),
                                       int(self.dicomR.dicomSizePixel[2] / 2))
                    self.dicomR.zeroPos = (0, 0, 0)

                    self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 0)
                    self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 1)
                    self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 2)



    # def combine(self):
    #     num_points = len(self.points_a)
    #     K = np.zeros((num_points, num_points))

    #     for i in range(num_points):
    #         for j in range(num_points):
    #             K[i][j] = sum(np.subtract(self.points_a[i], self.points_b[j]) ** 2)
    #             K[j][i] = K[i][j]

    #     K = np.maximum(K, 1e-320)

    #     K = np.sqrt(K)

    #     P = np.hstack((np.ones((num_points, 1)), self.points_a))

    #     a1 = np.hstack((K, P))
    #     a2 = np.hstack((np.transpose(P), np.zeros((4, 4))))

    #     L = np.vstack((a1, a2))

    #     param = np.matmul(np.linalg.pinv(L), np.vstack((self.points_b, np.zeros((4, 3)))))

    #     #####################################################################################

    #     # new_volume = np.zeros_like(self.dicomB.dicomData)

    #     K = np.zeros((len(self.dicomB.dicomData), num_points))

    #     gx = self.dicomB.dicomData[:][0]
    #     gy = self.dicomB.dicomData[:][1]
    #     gz = self.dicomB.dicomData[:][2]

    #     for i in range(num_points):
    #         K[:][i] = (gx - self.points_a[i][0]) ** 2 + (gy - self.points_a[i][1]) ** 2 + (gz - self.points_a[i][2]) ** 2

    #     K = np.maximum(K, 1e-320)
    #     K = np.sqrt(K)

    #     P = np.hstack((np.hstack((np.hstack((np.ones((len(self.dicomB.dicomData), 1)), gx)), gy)), gz))

    #     L = np.hstack((K, P))

    #     new_volume = np.matmul(L, param)
    #     new_volume[:][0] = np.round(new_volume[:][0] * (1e3)) * (1e-3)

    #     self.dicomR = DicomClass()
    #     self.dicomR.dicomData = new_volume  #
    #     self.dicomR.ct1 = new_volume  #
    #     self.dicomR.dicomSizePixel = new_volume.shape  #
    #     self.dicomR.scaleM = self.dicom.scaleM
    #     self.dicomR.scale = self.dicom.scale
    #     self.dicomR.pos = (10, 10, 10)
    #     self.dicomR.zeroPos = (0, 0, 0)
    #     # self.dicomR.dicomSizeMM = np.maximum(self.dicom.dicomSizeMM,self.dicomB.dicomSizeMM)
    #     self.dicomR.dicomSizeMM = new_volume.shape  #
    #     dicomRtemp = self.dicomR
    #     Settings.myList.append(dicomRtemp)

    #     self.dicomR.pos = (int(self.dicomR.dicomSizePixel[0] / 2), int(self.dicomR.dicomSizePixel[1] / 2),
    #                        int(self.dicomR.dicomSizePixel[2] / 2))
    #     self.dicomR.zeroPos = (0, 0, 0)

    #     self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 0)
    #     self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 1)
    #     self.ShowDicomR(self.dicomR.dicomData, self.dicomR.pos, 2)


    def sendMain(self):
        if (self.dicomR is not None):
            self.parent.dicomR = self.dicomR
            self.parent.setZeroButton.setEnabled(True)
            self.parent.resliceButton.setEnabled(True)
            # self.parent.QIButton.setEnabled(True)
            self.signal.connect(self.parent.receiveCoReg)
            self.signal.emit()
