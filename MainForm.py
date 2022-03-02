""""
pyRecAid

Written by Hamed Heidari (hamed.h@live.com).
Updated by Pouya Narimani (pouya.narimani@ut.ac.ir).

(c) Copyright BCoLab, All Rights Reserved. NO WARRANTY.

"""


# from contextlib import contextmanager
# from PyQt5 import QtWidgets, QtCore, QtGui
# import Settings

import scipy.ndimage
import math
from DicomClass import *
from NiftiClass import *
from ResliceForm import *
from CoregistrationForm import *
from ChamberClass import *
from ResliceData import *
import pickle
import subprocess
import copy
from skimage import draw

import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QApplication

# from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# from skimage import measure


class MainForm(QtWidgets.QMainWindow):
    dicom = None
    signal = QtCore.pyqtSignal()
    beginDistance = (0, 0, 0)
    endDistance = (0, 0, 0)

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.initUI()

    def initUI(self):
        Settings.init()  # Call only once

        self.setGeometry(20, 50, 1650, 920)
        self.setWindowTitle('pyRecAid: Main')
        self.setMinimumSize(1760, 980)
        self.statusBar()

        # layoutGrid = QGridLayout()
        # self.setLayout(layoutGrid)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        # self.Quality = False

        # list
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.move(50, 70)
        self.listWidget.resize(300, 200)

        # region Buttons
        # button
        self.openDir = QPushButton("&Load Folder", self)
        self.openDir.move(67, 285)
        # self.openDir.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # layoutGrid.addWidget(self.openDir)
        self.openDir.clicked.connect(self.LoadDir)

        # button
        self.loadDataButton = QtWidgets.QPushButton("&Load Series", self)
        self.loadDataButton.move(233, 285)
        self.loadDataButton.clicked.connect(self.LoadData)
        self.loadDataButton.setEnabled(False)

        # button
        self.sendButton = QtWidgets.QPushButton("&Send", self)
        self.sendButton.move(1450, 500)
        self.sendButton.resize(110, 35)
        self.sendButton.clicked.connect(self.SendClickedEvent)
        self.sendButton.setEnabled(False)

        # button
        self.setZeroButton = QtWidgets.QPushButton("&Set Zero", self)
        self.setZeroButton.move(1280, 500)
        self.setZeroButton.resize(110, 35)
        self.setZeroButton.clicked.connect(self.SetZero)
        self.setZeroButton.setEnabled(False)

        # button
        # self.QIButton = QtWidgets.QPushButton("&Quality Improvment", self)
        # self.QIButton.move(110, 340)
        # self.QIButton.resize(180, 35)
        # self.QIButton.clicked.connect(self.QI)
        # self.QIButton.setEnabled(False)

        # button
        self.addButton = QtWidgets.QPushButton("&Coregistration", self)
        self.addButton.move(145, 400)
        self.addButton.resize(110, 35)
        self.addButton.clicked.connect(self.Coregistration)
        # self.addButton.setEnabled(False)

        # endregion

        # region ReSlice
        # group box
        self.RgroupBox = QtWidgets.QGroupBox('&Reslice option', self)
        self.RgroupBox.move(67, 510)
        self.RgroupBox.resize(266, 100)
        self.RgroupBox.hide()

        # spinbox
        # self.spinboxLabel0 = QtWidgets.QLabel("X:", self.groupBox)
        # self.spinboxLabel0.move(20, 25)
        # self.spinbox0 = QtWidgets.QSpinBox(self.groupBox)
        # self.spinbox0.move(40, 25)
        # self.spinbox0.setMinimum(-180)
        # self.spinbox0.setMaximum(180)
        # self.spinbox0.setValue(0)

        self.spinboxLabel1 = QtWidgets.QLabel("AP Angle:", self.RgroupBox)
        self.spinboxLabel1.move(5, 25)
        self.spinbox1 = QtWidgets.QSpinBox(self.RgroupBox)
        self.spinbox1.move(80, 25)
        self.spinbox1.setMinimum(-180)
        self.spinbox1.setMaximum(180)
        self.spinbox1.setValue(0)

        self.spinboxLabel2 = QtWidgets.QLabel("ML Angle:", self.RgroupBox)
        self.spinboxLabel2.move(130, 25)
        self.spinbox2 = QtWidgets.QSpinBox(self.RgroupBox)
        self.spinbox2.move(215, 25)
        self.spinbox2.setMinimum(-180)
        self.spinbox2.setMaximum(180)
        self.spinbox2.setValue(0)

        # button
        self.resliceButton = QtWidgets.QPushButton("&Reslice", self.RgroupBox)
        self.resliceButton.move(15, 60)
        self.resliceButton.resize(90, 30)
        self.resliceButton.clicked.connect(self.ResliceMethod)
        self.resliceButton.setEnabled(False)

        # button
        self.openLastReslice = QtWidgets.QPushButton("&Open Last Reslice", self.RgroupBox)
        self.openLastReslice.move(125, 60)
        self.openLastReslice.resize(130, 30)
        self.openLastReslice.clicked.connect(self.OpenLastReslice)
        self.openLastReslice.setEnabled(False)

        # endregion

        #  region flip
        self.flipReg = QtWidgets.QGroupBox('&Flip', self)
        self.flipReg.move(67, 650)
        self.flipReg.resize(266, 70)
        self.flipReg.hide()

        # button pouya
        self.flip_a = QtWidgets.QPushButton("Flip_H", self.flipReg)
        self.flip_a.resize(70, 30)
        self.flip_a.move(10, 30)
        self.flip_a.clicked.connect(self.my_flip_a)

        # button pouya
        self.flip_b = QtWidgets.QPushButton("Flip_S", self.flipReg)
        self.flip_b.resize(70, 30)
        self.flip_b.move(100, 30)
        self.flip_b.clicked.connect(self.my_flip_b)

        # button pouya
        self.flip_c = QtWidgets.QPushButton("Flip_C", self.flipReg)
        self.flip_c.resize(70, 30)
        self.flip_c.move(190, 30)
        self.flip_c.clicked.connect(self.my_flip_c)

        # region Chamber
        # group box
        self.groupBoxch = QtWidgets.QGroupBox('&Chamber Size', self)
        self.groupBoxch.move(67, 750)
        self.groupBoxch.resize(266, 130)
        self.groupBoxch.hide()

        # spinbox
        self.spinboxLabelch0 = QtWidgets.QLabel("depth:", self.groupBoxch)
        self.spinboxLabelch0.move(10, 25)
        self.spinboxch0 = QtWidgets.QSpinBox(self.groupBoxch)
        self.spinboxch0.move(40, 25)
        self.spinboxch0.setMinimum(0)
        self.spinboxch0.setMaximum(5000)
        self.spinboxch0.setValue(0)

        self.spinboxLabelch1 = QtWidgets.QLabel("ML:", self.groupBoxch)
        self.spinboxLabelch1.move(100, 25)
        self.spinboxch1 = QtWidgets.QSpinBox(self.groupBoxch)
        self.spinboxch1.move(120, 25)
        self.spinboxch1.setMinimum(0)
        self.spinboxch1.setMaximum(5000)
        self.spinboxch1.setValue(0)

        self.spinboxLabelch2 = QtWidgets.QLabel("AP:", self.groupBoxch)
        self.spinboxLabelch2.move(180, 25)
        self.spinboxch2 = QtWidgets.QSpinBox(self.groupBoxch)
        self.spinboxch2.move(200, 25)
        self.spinboxch2.setMinimum(0)
        self.spinboxch2.setMaximum(5000)
        self.spinboxch2.setValue(0)

        self.spinboxLabelch3 = QtWidgets.QLabel("Angle:", self.groupBoxch)
        self.spinboxLabelch3.move(10, 50)
        self.spinboxch3 = QtWidgets.QSpinBox(self.groupBoxch)
        self.spinboxch3.move(40, 50)
        self.spinboxch3.setMinimum(-180)
        self.spinboxch3.setMaximum(180)
        self.spinboxch3.setValue(0)

        self.spinboxLabelch4 = QtWidgets.QLabel("Angle:", self.groupBoxch)
        self.spinboxLabelch4.move(90, 50)
        self.spinboxch4 = QtWidgets.QSpinBox(self.groupBoxch)
        self.spinboxch4.move(120, 50)
        self.spinboxch4.setMinimum(-180)
        self.spinboxch4.setMaximum(180)
        self.spinboxch4.setValue(0)

        self.spinboxLabelch5 = QtWidgets.QLabel("Angle:", self.groupBoxch)
        self.spinboxLabelch5.move(170, 50)
        self.spinboxch5 = QtWidgets.QSpinBox(self.groupBoxch)
        self.spinboxch5.move(200, 50)
        self.spinboxch5.setMinimum(-180)
        self.spinboxch5.setMaximum(180)
        self.spinboxch5.setValue(0)

        # button
        self.addButton = QtWidgets.QPushButton("&Add Chamber", self.groupBoxch)
        self.addButton.move(15, 90)
        self.addButton.resize(110, 30)
        self.addButton.clicked.connect(self.AddChamber)
        # self.addButton.setEnabled(False)

        self.clearChamber = QtWidgets.QPushButton("&Clear Chamber", self.groupBoxch)
        self.clearChamber.move(145, 90)
        self.clearChamber.resize(110, 30)
        self.clearChamber.clicked.connect(self.ClearChamber)
        # self.addButton.setEnabled(False)

        # endregion

        # region Distane
        # group box Distance
        self.groupBoxDistance = QtWidgets.QGroupBox('&Distance', self)
        self.groupBoxDistance.move(1120, 540)
        self.groupBoxDistance.resize(600, 190)

        font1 = QtGui.QFont()
        font1.setPointSize(9)
        font1.setBold(True)

        # button
        self.beginDistanceButton = QtWidgets.QPushButton("&Set Begin Distance", self.groupBoxDistance)
        self.beginDistanceButton.move(20, 50)
        self.beginDistanceButton.resize(200, 25)
        self.beginDistanceButton.clicked.connect(self.BeginDistanceButton)

        self.beginDistanceLabel = QtWidgets.QLabel("Begin Distance:   0 , 0 , 0", self.groupBoxDistance)
        self.beginDistanceLabel.move(20, 20)
        self.beginDistanceLabel.resize(550, 18)
        self.beginDistanceLabel.setStyleSheet('QLabel {color: #3333AA;}')
        self.beginDistanceLabel.setFont(font1)

        # button
        self.endDistanceButton = QtWidgets.QPushButton("&Set End Distance", self.groupBoxDistance)
        # self.endDistanceButton.move(380, 100)
        # self.endDistanceButton.resize(120, 35)
        self.endDistanceButton.move(20, 130)
        self.endDistanceButton.resize(200, 25)
        self.endDistanceButton.clicked.connect(self.EndDistanceButton)

        self.endDistanceLabel = QtWidgets.QLabel("End Distance:     0 , 0 , 0", self.groupBoxDistance)
        self.endDistanceLabel.move(20, 100)
        self.endDistanceLabel.resize(550, 18)
        self.endDistanceLabel.setStyleSheet('QLabel {color: #AA3333;}')
        self.endDistanceLabel.setFont(font1)

        self.HorizontalAngleLabel = QtWidgets.QLabel("Medial-lateral  Angle = 0 degree", self.groupBoxDistance)
        self.HorizontalAngleLabel.move(320, 40)
        self.HorizontalAngleLabel.resize(250, 25)
        self.HorizontalAngleLabel.setStyleSheet('QLabel {color: #448844;}')
        self.HorizontalAngleLabel.setFont(font1)

        self.VerticalAngleLabel = QtWidgets.QLabel("Anterior-posterior  Angle = 0 degree", self.groupBoxDistance)
        self.VerticalAngleLabel.move(320, 85)
        self.VerticalAngleLabel.resize(250, 25)
        self.VerticalAngleLabel.setStyleSheet('QLabel {color: #448844;}')
        self.VerticalAngleLabel.setFont(font1)

        self.distanceLabel = QtWidgets.QLabel("Distance = 0 millimeter", self.groupBoxDistance)
        self.distanceLabel.move(320, 130)
        self.distanceLabel.resize(250, 25)
        self.distanceLabel.setStyleSheet('QLabel {color: #448844;}')
        self.distanceLabel.setFont(font1)

        # endregion2

        # region Distane1
        # group box Distance
        # self.groupBoxDistance1 = QtWidgets.QGroupBox('&Distance2', self)
        # self.groupBoxDistance1.move(1120, 740)
        # self.groupBoxDistance1.resize(600, 190)

        # font1 = QtGui.QFont()
        # font1.setPointSize(9)
        # font1.setBold(True)

        # # button
        # self.beginDistanceButton1 = QtWidgets.QPushButton("&Set Begin Point", self.groupBoxDistance1)
        # # self.beginDistanceButton1.move(80, 100)
        # # self.beginDistanceButton1.resize(120, 35)
        # self.beginDistanceButton1.move(320, 95)
        # self.beginDistanceButton1.resize(200, 25)
        # self.beginDistanceButton1.clicked.connect(self.BeginDistanceButton1)

        # self.beginDistanceLabel1 = QtWidgets.QLabel("Begin Distance:   0 , 0 , 0", self.groupBoxDistance1)
        # self.beginDistanceLabel1.move(320, 50)
        # self.beginDistanceLabel1.resize(550, 18)
        # self.beginDistanceLabel1.setStyleSheet('QLabel {color: #3333AA;}')
        # self.beginDistanceLabel1.setFont(font1)

        # # spinbox
        # self.spinboxLabel01 = QtWidgets.QLabel("Medial-lateral Angle:", self.groupBoxDistance1)
        # self.spinboxLabel01.move(20, 40)
        # self.lineEdit0 = QtWidgets.QLineEdit(self.groupBoxDistance1)
        # self.lineEdit0.move(150, 40)

        # self.spinboxLabel11 = QtWidgets.QLabel("Anterior-posterior Angle:", self.groupBoxDistance1)
        # self.spinboxLabel11.move(20, 70)
        # self.lineEdit1 = QtWidgets.QLineEdit(self.groupBoxDistance1)
        # self.lineEdit1.move(150, 70)

        # self.spinboxLabel21 = QtWidgets.QLabel("Distance (mm):", self.groupBoxDistance1)
        # self.spinboxLabel21.move(20, 100)
        # self.lineEdit2 = QtWidgets.QLineEdit(self.groupBoxDistance1)
        # self.lineEdit2.move(150, 100)

        # self.calculatesButton = QtWidgets.QPushButton("&calculates", self.groupBoxDistance1)
        # self.calculatesButton.move(250, 150)
        # self.calculatesButton.resize(100, 25)
        # self.calculatesButton.clicked.connect(self.CalculatesButton)
        # endregion

        # region Disp
        # img0
        self.img0 = QtWidgets.QLabel(self)
        self.img0.move(420, 70)
        self.img0.resize(600, 400)
        self.img0.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap = QtGui.QPixmap("dicom.png")
        self.img0.setPixmap(pixmap)
        self.img0.setScaledContents(1)
        self.img0.wheelEvent = self.wheelEventImg0Event
        self.img0.mouseDoubleClickEvent = self.DoubleClickEventImg0Event
        self.img0.setAlignment(QtCore.Qt.AlignCenter)
        # label0
        self.labelImg0 = QtWidgets.QLabel("", self)
        self.labelImg0.move(422, 72)
        self.labelImg0.resize(550, 18)
        self.labelImg0.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg0.setFont(font)

        self.labelImg00 = QtWidgets.QLabel("Horizontal", self)
        self.labelImg00.move(677, 20)
        self.labelImg00.resize(350, 30)
        self.labelImg00.setStyleSheet('QLabel {color: #888888;}')
        self.labelImg00.setFont(font)

        self.labelImg00 = QtWidgets.QLabel("R", self)
        self.labelImg00.move(1021, 255)
        self.labelImg00.resize(350, 30)
        self.labelImg00.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg00.setFont(font)

        self.labelImg00 = QtWidgets.QLabel("L", self)
        self.labelImg00.move(407, 255)
        self.labelImg00.resize(350, 30)
        self.labelImg00.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg00.setFont(font)

        self.labelImg00 = QtWidgets.QLabel("P", self)
        self.labelImg00.move(714, 465)
        self.labelImg00.resize(350, 30)
        self.labelImg00.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg00.setFont(font)

        self.labelImg00 = QtWidgets.QLabel("A", self)
        self.labelImg00.move(714, 45)
        self.labelImg00.resize(350, 30)
        self.labelImg00.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg00.setFont(font)

        # img1
        self.img1 = QtWidgets.QLabel(self)
        self.img1.move(1120, 70)
        self.img1.resize(600, 400)
        self.img1.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap2 = QtGui.QPixmap("dicom.png")
        self.img1.setPixmap(pixmap2)
        self.img1.setScaledContents(1)
        self.img1.wheelEvent = self.wheelEventImg1Event
        self.img1.mouseDoubleClickEvent = self.DoubleClickEventImg1Event
        self.img1.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImg1 = QtWidgets.QLabel("", self)
        self.labelImg1.move(1122, 72)
        self.labelImg1.resize(550, 18)
        self.labelImg1.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg1.setFont(font)

        self.labelImg11 = QtWidgets.QLabel("Sagittal", self)
        self.labelImg11.move(1385, 20)
        self.labelImg11.resize(350, 30)
        self.labelImg11.setStyleSheet('QLabel {color: #888888;}')
        self.labelImg11.setFont(font)

        self.labelImg11 = QtWidgets.QLabel("A", self)
        self.labelImg11.move(1722, 255)
        self.labelImg11.resize(350, 30)
        self.labelImg11.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg11.setFont(font)

        self.labelImg11 = QtWidgets.QLabel("P", self)
        self.labelImg11.move(1106, 255)
        self.labelImg11.resize(350, 30)
        self.labelImg11.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg11.setFont(font)

        self.labelImg11 = QtWidgets.QLabel("D", self)
        self.labelImg11.move(1415, 45)
        self.labelImg11.resize(350, 30)
        self.labelImg11.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg11.setFont(font)

        self.labelImg11 = QtWidgets.QLabel("V", self)
        self.labelImg11.move(1415, 465)
        self.labelImg11.resize(350, 30)
        self.labelImg11.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg11.setFont(font)

        # img2
        self.img2 = QtWidgets.QLabel(self)
        self.img2.move(420, 530)
        self.img2.resize(600, 400)
        self.img2.setStyleSheet('QLabel {background-color: #000000;}')
        pixmap3 = QtGui.QPixmap("dicom.png")
        self.img2.setPixmap(pixmap3)
        self.img2.setScaledContents(1)
        self.img2.wheelEvent = self.wheelEventImg2Event
        self.img2.mouseDoubleClickEvent = self.DoubleClickEventImg2Event
        self.img2.setAlignment(QtCore.Qt.AlignCenter)
        # label1
        self.labelImg2 = QtWidgets.QLabel("", self)
        self.labelImg2.move(422, 532)
        self.labelImg2.resize(550, 18)
        self.labelImg2.setStyleSheet('QLabel {color: #FFFFFF;}')
        self.labelImg2.setFont(font)

        self.labelImg22 = QtWidgets.QLabel("Coronal", self)
        self.labelImg22.move(685, 485)
        self.labelImg22.resize(350, 30)
        self.labelImg22.setStyleSheet('QLabel {color: #888888;}')
        self.labelImg22.setFont(font)

        self.labelImg22 = QtWidgets.QLabel("D", self)
        self.labelImg22.move(714, 505)
        self.labelImg22.resize(350, 30)
        self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg22.setFont(font)

        self.labelImg22 = QtWidgets.QLabel("V", self)
        self.labelImg22.move(714, 925)
        self.labelImg22.resize(350, 30)
        self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg22.setFont(font)

        self.labelImg22 = QtWidgets.QLabel("R", self)
        self.labelImg22.move(406, 715)
        self.labelImg22.resize(350, 30)
        self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg22.setFont(font)

        self.labelImg22 = QtWidgets.QLabel("L", self)
        self.labelImg22.move(1021, 715)
        self.labelImg22.resize(350, 30)
        self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        self.labelImg22.setFont(font)


        # # img3
        # self.img3 = QtWidgets.QLabel(self)
        # self.img3.move(1120, 530)
        # self.img3.resize(600, 400)
        # self.img3.setStyleSheet('QLabel {background-color: #000000;}')
        # pixmap4 = QtGui.QPixmap("dicom.png")
        # self.img3.setPixmap(pixmap4)
        # self.img3.setScaledContents(1)
        # # self.img3.wheelEvent = self.wheelEventImg2Event
        # # self.img3.mouseDoubleClickEvent = self.DoubleClickEventImg2Event
        # self.img3.setAlignment(QtCore.Qt.AlignCenter)
        # # label1
        # self.labelImg3 = QtWidgets.QLabel("", self)
        # self.labelImg3.move(422, 532)
        # self.labelImg3.resize(550, 18)
        # self.labelImg3.setStyleSheet('QLabel {color: #FFFFFF;}')
        # self.labelImg3.setFont(font)

        # self.labelImg22 = QtWidgets.QLabel("Coronal", self)
        # self.labelImg22.move(685, 485)
        # self.labelImg22.resize(350, 30)
        # self.labelImg22.setStyleSheet('QLabel {color: #888888;}')
        # self.labelImg22.setFont(font)

        # self.labelImg22 = QtWidgets.QLabel("D", self)
        # self.labelImg22.move(714, 505)
        # self.labelImg22.resize(350, 30)
        # self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        # self.labelImg22.setFont(font)

        # self.labelImg22 = QtWidgets.QLabel("V", self)
        # self.labelImg22.move(714, 925)
        # self.labelImg22.resize(350, 30)
        # self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        # self.labelImg22.setFont(font)

        # self.labelImg22 = QtWidgets.QLabel("R", self)
        # self.labelImg22.move(406, 715)
        # self.labelImg22.resize(350, 30)
        # self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        # self.labelImg22.setFont(font)

        # self.labelImg22 = QtWidgets.QLabel("L", self)
        # self.labelImg22.move(1021, 715)
        # self.labelImg22.resize(350, 30)
        # self.labelImg22.setStyleSheet('QLabel {color: #222222;}')
        # self.labelImg22.setFont(font)


        # img3
        # self.img3 = QtWidgets.QLabel(self)
        # self.img3.move(1020, 480)
        # self.img3.resize(600, 400)
        # self.img3.setStyleSheet('QLabel {background-color: #000000;}')
        # pixmap4 = QtGui.QPixmap("dicom.png")
        # self.img3.setPixmap(pixmap4)
        # self.img3.setScaledContents(1)
        # endregion

        # region Menu
        LoadFile = QtWidgets.QAction(QtGui.QIcon('Load.png'), 'Load Directory', self)
        LoadFile.setShortcut('Ctrl+L')
        LoadFile.setStatusTip('Load Directory')
        LoadFile.triggered.connect(self.LoadDir)

        openFile = QtWidgets.QAction(QtGui.QIcon('open.png'), 'open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Save new File')
        openFile.triggered.connect(self.LoadFile)

        saveFile = QtWidgets.QAction(QtGui.QIcon('Save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save new File')
        saveFile.triggered.connect(self.SaveFile)

        coreg = QtWidgets.QAction(QtGui.QIcon('open.png'), 'Coregistration', self)
        coreg.setShortcut('Ctrl+D')
        coreg.setStatusTip('coregistration')
        coreg.triggered.connect(self.Coregistration)

        coregPet = QtWidgets.QAction(QtGui.QIcon('open.png'), 'CoRegistration(PET)', self)
        coregPet.setShortcut('Ctrl+D')
        coregPet.setStatusTip('coregistration')
        coregPet.triggered.connect(self.CoregistrationPet)

        resliceOptions = QtWidgets.QAction('Reslice', self)
        resliceOptions.setCheckable(True)
        resliceOptions.setStatusTip('reslice')
        resliceOptions.triggered.connect(self.resliceOptions)
        # resliceOptions.setEnabled(False)

        flipMenu = QtWidgets.QAction('Flip', self)
        flipMenu.setCheckable(True)
        flipMenu.setStatusTip('flip')
        flipMenu.triggered.connect(self.FlipMenu)
        # flipMenu.setEnabled(False)

        addChamberMenu = QtWidgets.QAction('Add chamber', self)
        addChamberMenu.setStatusTip('add chamber')
        addChamberMenu.setCheckable(True)
        addChamberMenu.triggered.connect(self.AddChamberMenu)
        # addChamberMenu.setEnabled(False)

        # newLogMenu = QtWidgets.QAction('New Log', self)
        # # newLogMenu.triggered.connect(self.newLog)
        # newLogMenu.setEnabled(False)

        # selectLogMenu = QtWidgets.QAction('Select Log', self)
        # # selectLogMenu.triggered.connect(self.selectLog)
        # selectLogMenu.setEnabled(False)

        # viewLog = QtWidgets.QAction('View Log', self)
        # viewLog.triggered.connect(self.viewLog)

        manual = QtWidgets.QAction('manual', self)
        manual.setShortcut('Ctrl+h')
        manual.triggered.connect(self.manual)

        aboutMenu = QtWidgets.QAction('about', self)
        aboutMenu.triggered.connect(self.about)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        toolsMenu = menubar.addMenu('&Tools')
        helpMenu = menubar.addMenu('&Help')

        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        fileMenu.addAction(LoadFile)
        toolsMenu.addAction(coreg)
        # toolsMenu.addAction(coregPet)
        # toolsMenu.addAction(setZeroMenu)
        # toolsMenu.addAction(resliceMenu)
        # toolsMenu.addAction(newLogMenu)
        # toolsMenu.addAction(selectLogMenu)
        # toolsMenu.addAction(viewLog)
        toolsMenu.addAction(resliceOptions)
        toolsMenu.addAction(flipMenu)
        toolsMenu.addAction(addChamberMenu)
        helpMenu.addAction(manual)
        helpMenu.addAction(aboutMenu)
        # endregion

        # def close(self):
        #     for childQWidget in self.findChildren(QtGui.QWidget):
        #         childQWidget.close()
        #     self.isDirectlyClose = True
        #     return QtGui.QMainWindow.close(self)

        # self.sendPoints = []


        self.Rflag = False
        self.Fflag = False
        self.Aflag = False

    def resliceOptions(self):
        if self.Rflag:
            self.RgroupBox.hide()
            self.Rflag = False
        else:
            self.RgroupBox.show()
            self.Rflag = True

    def FlipMenu(self):
        if self.Fflag:
            self.flipReg.hide()
            self.Fflag = False
        else:
            self.flipReg.show()
            self.Fflag = True

    def AddChamberMenu(self):
        if self.Aflag:
            self.groupBoxch.hide()
            self.Aflag = False
        else:
            self.groupBoxch.show()
            self.Aflag = True

    def closeEvent(self, eventQCloseEvent):
        eventQCloseEvent.ignore()
        answer = QtWidgets.QMessageBox.question(
            self,
            'quit',
            'Are you sure you want to quit ?',
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No)
        if (answer == QtWidgets.QMessageBox.Yes):
            QtCore.QCoreApplication.exit(0)
            # eventQCloseEvent.accept()
        else:
            eventQCloseEvent.ignore()
            # self.close()

    @contextmanager
    def WaitCursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

        coreg = []

    def Coregistration(self):
        self.coreg = CoregistrationForm(self)
        self.coreg.dicomR = None
        self.coreg.parent = self
        self.coreg.show()

    def CoregistrationPet(self):
        aa = self.coreg.hamed
        self.coreg2 = CoregistrationForm2(self)
        self.coreg2.show()

    def LoadDir(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        try:
            try:
                with self.WaitCursor():
                    if fname[0]:
                        self.listWidget.clear()
                        self.dicom = DicomClass()
                        # print('ok1')
                        xx = self.dicom.DicomSelect(fname)
                        # print(xx)
                        for i in range(len(xx)):
                            item = QtWidgets.QListWidgetItem(xx[i])
                            self.listWidget.addItem(item)
                    if (~self.loadDataButton.isEnabled()):
                        self.loadDataButton.setEnabled(True)
                    self.dicom.dicomClassState = 1
            except:
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
                    self.dicom.dicomClassState = 1
        except:
            time.sleep(0.001)

    def LoadData(self):
        try:
            try:
                value = int(self.listWidget.currentItem().text()[0:2])
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
                    self.setZeroButton.setEnabled(True)
                    self.resliceButton.setEnabled(True)
                    self.dicom.dicomClassState = 2
                    # self.QIButton.setEnabled(True)

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
                    self.setZeroButton.setEnabled(True)
                    self.resliceButton.setEnabled(True)
                    self.dicom.dicomClassState = 2

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Dicom Series is not correct')
            msg.exec_()

    def SaveFile(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(filter='*.dcmf')
        try:
            with self.WaitCursor():
                if fname[0]:
                    with open(fname[0], 'wb') as handle:
                        # self.dicom=DicomClass()
                        pickle.dump(self.dicom, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    # pickle.dump(self.dicom, open(fname[0], "wb"))
        except:
            time.sleep(0.001)

    def LoadFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(filter='*.dcmf')
        try:
            with self.WaitCursor():
                if fname[0]:
                    with open(fname[0], 'rb') as handle:
                        # unpickler = pickle.Unpickler(handle)
                        self.dicom = pickle.load(handle)
                        # self.dicom=DicomClass()
                        # self.dicom = unpickler.load()
                        # print(np.shape(self.dicom))
                        # print(self.dicom)
                        # print('----------------------------')
                        self.setZeroButton.setEnabled(True)
                        self.resliceButton.setEnabled(True)
                    if self.dicom.isResliceExist:
                        self.openLastReslice.setEnabled(True)
                        self.sendButton.setEnabled(True)
                    # if self.dicom.dicomClassState == 2:
                    #     self.resliceButton.setEnabled(True)
                    #     self.setZeroButton.setEnabled(True)

        except Exception as inst:
            # print(type(inst))  # the exception instance
            # print(inst.args)  # arguments stored in .args
            # print(inst)
            time.sleep(0.001)

    def plot_3d(self, image, threshold=50): 
        p = image.transpose(2,1,0)
        verts, faces, normals, values = measure.marching_cubes_lewiner(p, threshold)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        mesh = Poly3DCollection(verts[faces], alpha=0.1)
        face_color = [0.5, 0.5, 1]
        mesh.set_facecolor(face_color)
        ax.add_collection3d(mesh)
        ax.set_xlim(0, p.shape[0])
        ax.set_ylim(0, p.shape[1])
        ax.set_zlim(0, p.shape[2])

        plt.show()

    def Rotation1(self, inp, a, b, c):
        tempDicom = scipy.ndimage.rotate(inp, a, axes=(1, 2), reshape=True, output=np.uint8, order=1,
                                         mode='constant', prefilter=True)
        tempDicom = scipy.ndimage.rotate(tempDicom, b, axes=(0, 2), reshape=True, output=np.uint8, order=1,
                                         mode='constant', prefilter=True)
        tempDicom = scipy.ndimage.rotate(tempDicom, c, axes=(0, 1), reshape=True, output=np.uint8, order=1,
                                         mode='constant', prefilter=True)
        return tempDicom

    def Rotation2(self, inp, a, b, c):
        alpha = np.deg2rad(45)
        beta = np.deg2rad(45)
        gamma = np.deg2rad(45)
        a = []
        bb = []
        RX = np.array([[1, 0, 0], [0, np.cos(alpha), -np.sin(alpha)], [0, np.sin(alpha), np.cos(alpha)]])
        RY = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
        RZ = np.array([[np.cos(gamma), -np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
        R = np.dot(np.dot(RZ, RY), RX)
        sh = np.shape(inp)
        for i in range(sh[0]):
            for j in range(sh[1]):
                for k in range(sh[2]):
                    a.append(np.dot(R, (i, j, k)))
                    bb.append(self.dicom.dicomData[i, j, k])

        b = np.round(a) - np.min(np.round(a))
        c0 = int(np.max(b[:, 0]))
        c1 = int(np.max(b[:, 1]))
        c2 = int(np.max(b[:, 2]))
        d = np.zeros((int(c0) + 1, int(c1) + 1, int(c2) + 1))

        for i in range(b.shape[0]):
            d[int(b[i, 0]), int(b[i, 1]), int(b[i, 2])] = bb[i]
        return d

    def ResliceMethod(self):
        a = 0
        # self.spinbox0.value()
        b = self.spinbox1.value()
        c = self.spinbox2.value()

        self.dicom.reslice = (a, b, c)

        with self.WaitCursor():
            tempDicom = self.dicom.dicomData
            tempmap = np.zeros(np.shape(self.dicom.dicomData))
            tempmap[self.dicom.zeroPos] = 255
            tempDicom = self.Rotation1(tempDicom, a, b, c)

            tempmap = scipy.ndimage.rotate(tempmap, a, axes=(1, 2), reshape=True, output=np.uint8, order=1,
                                           mode='constant', prefilter=True)
            tempmap = scipy.ndimage.rotate(tempmap, b, axes=(0, 2), reshape=True, output=np.uint8, order=1,
                                           mode='constant', prefilter=True)
            tempmap = scipy.ndimage.rotate(tempmap, c, axes=(0, 1), reshape=True, output=np.uint8, order=1,
                                           mode='constant', prefilter=True)

            newzero = (np.where(tempmap == np.max(tempmap))[0][0], np.where(tempmap == np.max(tempmap))[1][0],
                       np.where(tempmap == np.max(tempmap))[2][0])

            # newzero = self.dicom.pos

            cc = np.dot(self.computeRotCam(a, b, c), self.dicom.zeroPos)

            self.dicom.dicomDataReslice = tempDicom
            # self.dicom.dicomDataReslice.append(tempDicom)
            self.resliceForm = ResliceForm(self, a, b, c, newzero, self.dicom.scaleM, self.dicom.dicomSizeMM,
                                           tempDicom)

            self.resliceForm.show()
            self.sendButton.setEnabled(True)
            self.openLastReslice.setEnabled(True)
            self.dicom.isResliceExist = True

    def OpenLastReslice(self):
        if self.dicom.isResliceExist:
            (a, b, c) = self.dicom.reslice
            tempmap = np.zeros(np.shape(self.dicom.dicomData))
            tempmap[self.dicom.zeroPos] = 255
            tempmap = scipy.ndimage.rotate(tempmap, a, axes=(1, 2), reshape=True, output=np.uint8, order=1,
                                           mode='constant', prefilter=True)
            tempmap = scipy.ndimage.rotate(tempmap, b, axes=(0, 2), reshape=True, output=np.uint8, order=1,
                                           mode='constant', prefilter=True)
            tempmap = scipy.ndimage.rotate(tempmap, c, axes=(0, 1), reshape=True, output=np.uint8, order=1,
                                           mode='constant', prefilter=True)

            tempDicom = self.dicom.dicomDataReslice

            newzero = (np.where(tempmap == np.max(tempmap))[0][0], np.where(tempmap == np.max(tempmap))[1][0],
                       np.where(tempmap == np.max(tempmap))[2][0])
            cc = np.dot(self.computeRotCam(a, b, c), self.dicom.zeroPos)
            self.resliceForm = ResliceForm(self, a, b, c, newzero, self.dicom.scaleM, self.dicom.dicomSizeMM, tempDicom)
            self.resliceForm.show()

    def computeRotCam(self, alpha1=0.0, beta1=0.0, gamma1=0.0):
        alpha = np.deg2rad(alpha1)
        beta = np.deg2rad(beta1)
        gamma = np.deg2rad(beta1)

        RX = np.array([[1, 0, 0], [0, np.cos(alpha), -np.sin(alpha)], [0, np.sin(alpha), np.cos(alpha)]])
        RY = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
        RZ = np.array([[np.cos(gamma), -np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
        return np.dot(RX, np.dot(RY, RZ))

    def unit_vector(self, data, axis=None, out=None):
        if out is None:
            data = np.array(data, dtype=np.float64, copy=True)
            if data.ndim == 1:
                data /= math.sqrt(np.dot(data, data))
                return data
        else:
            if out is not data:
                out[:] = np.array(data, copy=False)
            data = out
        length = np.atleast_1d(np.sum(data * data, axis))
        np.sqrt(length, length)
        if axis is not None:
            length = np.expand_dims(length, axis)
        data /= length
        if out is None:
            return data

    def rotation_matrix(self, angle, direction, point=None):
        sina = math.sin(angle)
        cosa = math.cos(angle)
        direction = self.unit_vector(direction[:3])
        # rotation matrix around unit vector
        R = np.diag([cosa, cosa, cosa])
        R += np.outer(direction, direction) * (1.0 - cosa)
        direction *= sina
        R += np.array([[0.0, -direction[2], direction[1]],
                       [direction[2], 0.0, -direction[0]],
                       [-direction[1], direction[0], 0.0]])
        M = np.identity(4)
        M[:3, :3] = R
        if point is not None:
            # rotation not around origin
            point = np.array(point[:3], dtype=np.float64, copy=False)
            M[:3, 3] = point - np.dot(R, point)
        return M

    def SetZero(self):
        self.dicom.zeroPos = self.dicom.pos
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    def array_to_qimage(self, arr, copy=False):
        """
        Convert NumPy array to QImage object

        :param numpy.array arr: NumPy array
        :param bool copy: if True, make a copy of the array
        :return: QImage object
        """
        # https://gist.githubusercontent.com/smex/5287589/raw/toQImage.py
        if arr is None:
            return QtGui.QImage()
        if len(arr.shape) not in (2, 3):
            raise NotImplementedError("Unsupported array shape %r" % arr.shape)
        data = arr.data
        ny, nx = arr.shape[:2]
        stride = arr.strides[0]  # bytes per line
        color_dim = None
        if len(arr.shape) == 3:
            color_dim = arr.shape[2]
        if arr.dtype == np.uint8:
            if color_dim is None:
                qimage = QtGui.QImage(data, nx, ny, stride, QtGui.QImage.Format_Indexed8)
                #            qimage.setColorTable([qRgb(i, i, i) for i in range(256)])
                qimage.setColorCount(256)
            elif color_dim == 3:
                qimage = QtGui.QImage(data, nx, ny, stride, QtGui.QImage.Format_RGB888)
            elif color_dim == 4:
                qimage = QtGui.QImage(data, nx, ny, stride, QtGui.QImage.Format_ARGB32)
            else:
                raise TypeError("Invalid third axis dimension (%r)" % color_dim)
        elif arr.dtype == np.uint32:
            qimage = QtGui.QImage(data, nx, ny, stride, QtGui.QImage.Format_ARGB32)
        else:
            raise NotImplementedError("Unsupported array data type %r" % arr.dtype)
        if copy:
            return qimage.copy()
        return qimage

    def ShowDicom(self, ct, pos, frame):
        diSize = np.shape(ct)
        a0 = np.transpose(ct[pos[0], :, :], (1, 0))
        a1 = np.transpose(ct[:, pos[1], :], (0, 1))
        a2 = ct[:, :, pos[2]]

        a0 = cv2.rotate(a0, cv2.ROTATE_180)

        # print(ct.min(), ct.max())

        # a0 = cv2.equalizeHist(a0)
        # a1 = cv2.equalizeHist(a1)
        # a2 = cv2.equalizeHist(a2)

        # if len(self.dicom.dicom_chamber)>0:
        #     # print('\nok\n')
        #     # print(self.dicom.dicom_chamber)
        #     a2 = self.dicom.dicom_chamber[:, :, pos[2]]

        # hist = plt.hist(a0.reshape((-1, 1)), density=True, bins=256)
        
        # print(np.shape(plt.hist(a0.reshape((-1, 1)), density=True, bins=256)[0]))
        # print(np.shape(plt.hist(a0.reshape((-1, 1)), density=True, bins=256)[1]))
        # print(np.shape(plt.hist(a0.reshape((-1, 1)), density=True, bins=256)[2]))
        # plt.show()

        # if self.Quality:
        #     # Histogram Equalization
        #     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        #     a0 = clahe.apply(a0)
        #     a1 = clahe.apply(a1)
        #     a2 = clahe.apply(a2)

        #     # Denoising
        #     a0 = cv2.medianBlur(a0,3)
        #     a1 = cv2.medianBlur(a1,3)
        #     a2 = cv2.medianBlur(a2,3)


        pix0 = self.CreateQPixmap(a0, round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]),
                                  round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]), pos[2], pos[1],
                                  self.dicom.markerPos[2], self.dicom.markerPos[1], 2, 1, self.dicom.markerFlag)
        pix1 = self.CreateQPixmap(a1, round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                  round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2]), pos[0], pos[2],
                                  self.dicom.markerPos[0], self.dicom.markerPos[2], 0, 2, self.dicom.markerFlag)
        pix2 = self.CreateQPixmap(a2, round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                  round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]), pos[0], pos[1],
                                  self.dicom.markerPos[0], self.dicom.markerPos[1], 0, 1, self.dicom.markerFlag)
        # if self.has_chamber:
        #     sss = np.shape(self.dicom.dicom_chamber)
        #     pix3 = self.CreateQPixmap(self.dicom.dicom_chamber[:,:,self.dicom.dicom_chamber_pos[2]], round(self.dicom.dicom_chamber_scale[0] * sss[0]),
        #                               round(self.dicom.dicom_chamber_scale[1] * sss[1]), pos[0], pos[1],
        #                               self.dicom.markerPos[0], self.dicom.markerPos[1], 0, 1, self.dicom.markerFlag)


        self.img0.setPixmap(pix0)
        self.img0.setScaledContents(1)
        self.img1.setPixmap(pix1)
        self.img1.setScaledContents(1)
        self.img2.setPixmap(pix2)
        self.img2.setScaledContents(1)
        # if self.has_chamber:
        #     self.img3.setPixmap(pix3)
        #     self.img3.setScaledContents(1)

        if frame == 0:
            if self.dicom.zeroPos[0] == 0:
                self.labelImg0.setText(str(round((pos[0] - self.dicom.zeroPos[0]) * self.dicom.scaleM[0], 2)) + "mm")
            else:
                self.labelImg0.setText(str(round((self.dicom.zeroPos[0] - pos[0]) * self.dicom.scaleM[0], 2)) + "mm")
        if frame == 1:
            self.labelImg1.setText(str(round((pos[1] - self.dicom.zeroPos[1]) * self.dicom.scaleM[1], 2)) + "mm")
        if frame == 2:
            self.labelImg2.setText(str(round((pos[2] - self.dicom.zeroPos[2]) * self.dicom.scaleM[2], 2)) + "mm")

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
                        # self.dicom.dicom_chamber_pos = (self.dicom.dicom_chamber_pos[0]+1, self.dicom.dicom_chamber_pos[1], self.dicom.dicom_chamber_pos[2])
                        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[0] > 0):
                        self.dicom.pos = (self.dicom.pos[0] - 1, self.dicom.pos[1], self.dicom.pos[2])
                        # self.dicom.dicom_chamber_pos = (self.dicom.dicom_chamber_pos[0]-1, self.dicom.dicom_chamber_pos[1], self.dicom.dicom_chamber_pos[2])
                        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)

    def wheelEventImg1Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicom.pos[1] < self.dicom.dicomSizePixel[1] - 1):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1] + 1, self.dicom.pos[2])
                        # self.dicom.dicom_chamber_pos = (self.dicom.dicom_chamber_pos[0], self.dicom.dicom_chamber_pos[1]+1, self.dicom.dicom_chamber_pos[2])
                        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[1] > 0):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1] - 1, self.dicom.pos[2])
                        # self.dicom.dicom_chamber_pos = (self.dicom.dicom_chamber_pos[0], self.dicom.dicom_chamber_pos[1]-1, self.dicom.dicom_chamber_pos[2])
                        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)

    def wheelEventImg2Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                numPixels = event.pixelDelta()
                numDegrees = event.angleDelta() / 8
                if (numDegrees.y() > 0):
                    if (self.dicom.pos[2] < self.dicom.dicomSizePixel[2] - 1):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1], self.dicom.pos[2] + 1)
                        # self.dicom.dicom_chamber_pos = (self.dicom.dicom_chamber_pos[0], self.dicom.dicom_chamber_pos[1], self.dicom.dicom_chamber_pos[2]+1)
                        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
                if (numDegrees.y() < 0):
                    if (self.dicom.pos[2] > 0):
                        self.dicom.pos = (self.dicom.pos[0], self.dicom.pos[1], self.dicom.pos[2] - 1)
                        # self.dicom.dicom_chamber_pos = (self.dicom.dicom_chamber_pos[0], self.dicom.dicom_chamber_pos[1], self.dicom.dicom_chamber_pos[2]-1)
                        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    def DoubleClickEventImg0Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a0 = np.transpose(self.dicom.dicomData[self.dicom.pos[0], :, :], (1, 0))
                a0 = cv2.resize(a0, (round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1]),
                                     round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2])),
                                interpolation=cv2.INTER_AREA)
                plt.imshow(a0, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg1Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a1 = np.transpose(self.dicom.dicomData[:, self.dicom.pos[1], :], (0, 1))
                a1 = cv2.resize(a1, (round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                     round(self.dicom.scale[2] * self.dicom.dicomSizePixel[2])),
                                interpolation=cv2.INTER_AREA)
                plt.imshow(a1, cmap=plt.cm.bone)
                plt.show()

    def DoubleClickEventImg2Event(self, event):
        if self.dicom is not None:
            if self.dicom.dicomData != []:
                a2 = self.dicom.dicomData[:, :, self.dicom.pos[2]]
                a2 = cv2.resize(a2, (round(self.dicom.scale[0] * self.dicom.dicomSizePixel[0]),
                                     round(self.dicom.scale[1] * self.dicom.dicomSizePixel[1])),
                                interpolation=cv2.INTER_AREA)
                plt.imshow(a2, cmap=plt.cm.bone)
                plt.show()

    def SendClickedEvent(self):
        with self.WaitCursor():
            self.dicom.markerPos = self.dicom.pos

            # point = (self.dicom.pos[0] * self.dicom.scaleM[0], self.dicom.pos[1] * self.dicom.scaleM[1], self.dicom.pos[2] * self.dicom.scaleM[2])
            # self.sendPoints.append(point)
            self.dicom.markerFlag = True

            # np.savetxt('SendPoints.txt', self.sendPoints, delimiter=',')

            tempmap = np.zeros(np.shape(self.dicom.dicomData))
            tempmap[self.dicom.markerPos] = 255
            (a, b, c) = self.dicom.reslice

            tempmap = scipy.ndimage.rotate(tempmap, a, axes=(1, 2), reshape=True, output=np.uint8, order=5,
                                           mode='constant', prefilter=True)
            tempmap = scipy.ndimage.rotate(tempmap, b, axes=(0, 2), reshape=True, output=np.uint8, order=5,
                                           mode='constant', prefilter=True)
            tempmap = scipy.ndimage.rotate(tempmap, c, axes=(0, 1), reshape=True, output=np.uint8, order=5,
                                           mode='constant', prefilter=True)
            newpos = (np.where(tempmap == np.max(tempmap))[0][0], np.where(tempmap == np.max(tempmap))[1][0],
                      np.where(tempmap == np.max(tempmap))[2][0])

            self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
            self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
            self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

            # self.resliceForm.sendZero=newpos
            self.resliceForm.sendMarker = newpos
            self.signal.connect(self.resliceForm.MainFormEvent)
            self.signal.emit()

    @QtCore.pyqtSlot()
    def receiveCoReg(self):
        a = 12
        self.dicom = self.dicomR
        self.dicom.dicomDataRaw = copy.deepcopy(self.dicom.dicomData)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    # chamber = []

    def AddChamber(self):
        try:
            self.chamber = ChamberClass(self.spinboxch0.value(), self.spinboxch1.value(), self.spinboxch2.value(),
                                        -self.spinboxch3.value(), -self.spinboxch4.value(), -self.spinboxch5.value(),
                                        self.dicom.pos[0], self.dicom.pos[1], self.dicom.pos[2])

            chamberPixelSize = [self.chamber.xSize / self.dicom.scaleM[0], self.chamber.ySize / self.dicom.scaleM[1],
                                self.chamber.zSize / self.dicom.scaleM[2]]
            ch = np.ones(np.round(chamberPixelSize).astype(int)) * 255

            ##################################################
            a = np.round(chamberPixelSize).astype(int)[0]
            b = np.round(chamberPixelSize).astype(int)[1]
            c = np.round(chamberPixelSize).astype(int)[2]
            r_radius = a / 2
            c_radius = b / 2
            ch = np.zeros((a, b, c))
            rr, cc = draw.ellipse(r_radius, c_radius, r_radius, c_radius, shape=ch.shape)
            ch[rr, cc, :] = 1
            ch = ch * 255
            #####################################################

            ch = self.Rotation1(ch, self.chamber.xAngle, self.chamber.yAngle, self.chamber.zAngle)

            chPixelSize = np.shape(ch)
            chPos = self.chamber.chamberPosition

            #############################################################################################
            
            # pouya_img = np.zeros(self.dicom.dicomSizePixel)
            # pouya_img[chPos[0] - chPixelSize[0]:chPos[0], chPos[1] - chPixelSize[1]:chPos[1],
            # chPos[2] - chPixelSize[2]:chPos[2]] = ch
            # # self.dicom.dicom_chamber = pouya_img
            # self.dicom.dicom_chamber = self.Rotation1(pouya_img, 0, 30, 30)
            # # self.dicom.dicom_chamber = np.resize(self.dicom.dicom_chamber, self.dicom.dicomSizePixel)

            # self.dicom.dicom_chamber_size = np.shape(self.dicom.dicom_chamber)
            # self.dicom.dicom_chamber_pos = (int(self.dicom.dicom_chamber_size[0]/2), int(self.dicom.dicom_chamber_size[1]/2), int(self.dicom.dicom_chamber_size[2]/2))
            # self.dicom.dicom_chamber_scale = (self.dicom.dicomSizePixel[0]/self.dicom.dicom_chamber_size[0], self.dicom.dicomSizePixel[1]/self.dicom.dicom_chamber_size[1], self.dicom.dicomSizePixel[2]/self.dicom.dicom_chamber_size[2])
            # self.has_chamber = True

            # print(self.dicom.dicom_chamber_size[0]*self.dicom.dicom_chamber_scale[0])

            #############################################################################################

            self.dicom.dicomData[chPos[0] - chPixelSize[0]:chPos[0], chPos[1] - chPixelSize[1]:chPos[1],
            chPos[2] - chPixelSize[2]:chPos[2]] = \
                np.maximum(ch,
                           self.dicom.dicomData[chPos[0] - chPixelSize[0]:chPos[0], chPos[1] - chPixelSize[1]:chPos[1],
                           chPos[2] - chPixelSize[2]:chPos[2]])
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Out of range!!!')
            msg.exec_()

    def ClearChamber(self):
        self.dicom.dicomData = []
        self.dicom.dicomData = copy.deepcopy(self.dicom.dicomDataRaw)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    def ComputeRotation(self, img, x, y, z):
        temp = img
        temp = scipy.ndimage.rotate(temp, x, axes=(0, 1), reshape=True, output=np.uint8, order=5, mode='constant',
                                    prefilter=True)
        temp = scipy.ndimage.rotate(temp, y, axes=(0, 2), reshape=True, output=np.uint8, order=5, mode='constant',
                                    prefilter=True)
        temp = scipy.ndimage.rotate(temp, z, axes=(1, 2), reshape=True, output=np.uint8, order=5, mode='constant',
                                    prefilter=True)
        return temp

    def ComputeNewPos(self, a, b, c, x, y, z, i, j, k):
        temp = np.zeros([a, b, c])
        temp[i, j, k] = 255
        temp = scipy.ndimage.rotate(temp, x, axes=(0, 1), reshape=True, output=np.uint8, order=5, mode='constant',
                                    prefilter=True)
        temp = scipy.ndimage.rotate(temp, y, axes=(0, 2), reshape=True, output=np.uint8, order=5, mode='constant',
                                    prefilter=True)
        temp = scipy.ndimage.rotate(temp, z, axes=(1, 2), reshape=True, output=np.uint8, order=5, mode='constant',
                                    prefilter=True)
        newpos = (np.where(temp == np.max(temp))[0][0], np.where(temp == np.max(temp))[1][0],
                  np.where(temp == np.max(temp))[2][0])
        return newpos

    # def Coregistration(self):
    #     # # self.dicom=self.dereg.dicomR
    #     # x=math.sqrt(math.pow(self.dicom.pos[0]-self.dicom.zeroPos[0],2)+math.pow(self.dicom.pos[1]-self.dicom.zeroPos[1],2)+math.pow(self.dicom.pos[2]-self.dicom.zeroPos[2],2))
    #     # msg = QtWidgets.QMessageBox()
    #     # msg.setIcon(QtWidgets.QMessageBox.Information)
    #     # msg.setWindowTitle("Error")
    #     # msg.setText(str(x))
    #     # msg.exec_()
    #     # print(1)
    #
    #     dicomRR=Settings.myList[0]
    #     self.dicom=dicomRR
    #     print(1)

    def BeginDistanceButton1(self):
        # self.beginDistance1=np.multiply(self.dicom.pos,self.dicom.scaleM)
        self.beginDistance1 = self.dicom.pos
        # tmp=np.round(np.multiply(self.dicom.pos,self.dicom.scaleM),2)
        self.beginDistanceLabel1.setText(
            "Begin Distance:   " + str(self.beginDistance1[0]) + " , " + str(self.beginDistance1[1]) + " , " + str(
                self.beginDistance1[2]))

        tmp = np.round(np.multiply(self.dicom.pos, self.dicom.scaleM), 2)

    def CalculatesButton(self):
        x = float(self.lineEdit0.text()) * math.pi / 180
        y = (float(self.lineEdit1.text()) + 90.0) * math.pi / 180
        d = float(self.lineEdit2.text())

        a0 = self.beginDistance1[0] + np.round(((d * math.cos(x) * math.sin(y))) / self.dicom.scaleM[0])
        a1 = self.beginDistance1[1] + np.round(((d * math.sin(x))) / self.dicom.scaleM[1])
        a2 = self.beginDistance1[2] + np.round(((d * math.cos(x) * math.cos(y))) / self.dicom.scaleM[2])

        self.dicom.markerPos = (int(a0), int(a1), int(a2))
        self.dicom.markerFlag = True
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
        self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    def BeginDistanceButton(self):
        self.beginDistance = np.multiply(self.dicom.pos, self.dicom.scaleM)
        x = math.sqrt(math.pow(self.endDistance[0] - self.beginDistance[0], 2) + math.pow(
            self.endDistance[1] - self.beginDistance[1], 2) + math.pow(self.endDistance[2] - self.beginDistance[2], 2))

        tmp = np.round(np.multiply(self.dicom.pos, self.dicom.scaleM), 2)
        self.beginDistanceLabel.setText("Begin Distance:   " + str(tmp[0]) + " , " + str(tmp[1]) + " , " + str(tmp[2]))

        angle0 = math.atan2(self.endDistance[0] - self.beginDistance[0],
                            self.endDistance[1] - self.beginDistance[1]) * 180 / math.pi
        angle1 = math.atan2(self.endDistance[0] - self.beginDistance[0],
                            self.endDistance[2] - self.beginDistance[2]) * 180 / math.pi

        if (np.array_equal(self.beginDistance, self.endDistance)):
            self.HorizontalAngleLabel.setText("Horizontal Angle = 0 degree")
            self.VerticalAngleLabel.setText("Vertical Angle = 0 degree")
        else:
            self.HorizontalAngleLabel.setText("Horizontal Angle = " + str(np.round(angle0 - 90, 2)) + " degree")
            self.VerticalAngleLabel.setText("Vertical Angle = " + str(np.round(angle1 - 90, 2)) + " degree")

        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)
        # msg.setWindowTitle("Error")
        # msg.setText(str(x))
        # msg.exec_()

    def EndDistanceButton(self):
        self.endDistance = np.multiply(self.dicom.pos, self.dicom.scaleM)
        x = math.sqrt(math.pow(self.endDistance[0] - self.beginDistance[0], 2) + math.pow(
            self.endDistance[1] - self.beginDistance[1], 2) + math.pow(self.endDistance[2] - self.beginDistance[2], 2))
        self.distanceLabel.setText("Distance = " + str(round(x, 4)) + " millimeter")
        tmp = np.round(np.multiply(self.dicom.pos, self.dicom.scaleM), 2)
        self.endDistanceLabel.setText("End Distance:     " + str(tmp[0]) + " , " + str(tmp[1]) + " , " + str(tmp[2]))

        angle0 = math.atan2(self.endDistance[0] - self.beginDistance[0],
                            self.endDistance[1] - self.beginDistance[1]) * 180 / math.pi
        angle1 = math.atan2(self.endDistance[0] - self.beginDistance[0],
                            self.endDistance[2] - self.beginDistance[2]) * 180 / math.pi

        if (np.array_equal(self.beginDistance, self.endDistance)):
            self.HorizontalAngleLabel.setText("Horizontal  Angle = 0 degree")
            self.VerticalAngleLabel.setText("Vertical Angle = 0 degree")
        else:
            self.HorizontalAngleLabel.setText("Horizontal  Angle = " + str(np.round(angle0 - 90, 2)) + " degree")
            self.VerticalAngleLabel.setText("Vertical Angle = " + str(np.round(angle1 - 90, 2)) + " degree")

    def about(self):

        about = QtWidgets.QMessageBox()
        about.setIcon(QtWidgets.QMessageBox.Information)
        about.setWindowTitle("About")
        about.setBaseSize(QtCore.QSize(700, 500))
        about.setMaximumSize(700, 500)

        text = \
            "this is pyRecAid; open-source python recording\n" + "utility for imaging guided intracranial access.\n" + \
            "first designed and developed in BCoL, SCS, IPM,\n" + "by Hamed Heidari and Farzad Shayanfar\n" + \
            "and updated by Pouya Narimani.\n" + \
            "for more information, please refer to the manual at help menu\n" + "\nversion: 0.5"
        about.setText(text)

        about_icon_label = QtWidgets.QLabel(about)
        if sys.platform == 'win32':
            icon = QtGui.QPixmap('Resource/Icon.png')
        else:
            icon = QtGui.QPixmap('Resource/Icon.png')
        about_icon_label.setPixmap(icon)
        about_icon_label.setScaledContents(True)
        about_icon_label.move(320, 15)
        about_icon_label.resize(70, 56)

        about.exec_()

    def manual(self):
        if sys.platform == 'win32':
            try:
                os.system('start ' + 'Resource/v_1.pdf')

            except:
                self.msg = Er_msg(self, msg='didn\'t manage to open the manual\n please open it yourself')

        else:
            try:
                subprocess.Popen(['evince', 'Resource/v_1.pdf'], stdin=False, stdout=False, stderr=False,
                                 close_fds=True)

            except:
                self.msg = Er_msg(self, msg='didn\'t manage to open the manual\n please open it yourself')

    def my_flip_a(self):
        if self.dicom is not None:
            if len(self.dicom.dicomData) != 0:
                for i in range(self.dicom.dicomSizePixel[0]):
                    self.dicom.dicomData[i, :, :] = np.flip(self.dicom.dicomData[i, :, :], axis=1)
                self.dicom.dicomDataRaw = copy.deepcopy(self.dicom.dicomData)

                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    def my_flip_b(self):
        if self.dicom is not None:
            if len(self.dicom.dicomData) != 0:
                for i in range(self.dicom.dicomSizePixel[1]):
                    self.dicom.dicomData[:, i, :] = np.flip(self.dicom.dicomData[:, i, :], axis=1)
                self.dicom.dicomDataRaw = copy.deepcopy(self.dicom.dicomData)

                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    def my_flip_c(self):
        if self.dicom is not None:
            if len(self.dicom.dicomData) != 0:
                for i in range(self.dicom.dicomSizePixel[2]):
                    self.dicom.dicomData[:, :, i] = np.flip(self.dicom.dicomData[:, :, i], axis=0)
                self.dicom.dicomDataRaw = copy.deepcopy(self.dicom.dicomData)

                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
                self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)

    # def QI(self):
    #     if self.dicom is not None:
    #         if len(self.dicom.dicomData) != 0:
    #             self.Quality = not(self.Quality)

    #             self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 0)
    #             self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 1)
    #             self.ShowDicom(self.dicom.dicomData, self.dicom.pos, 2)
