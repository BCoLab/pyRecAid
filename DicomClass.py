""""
pyRECaid

Written by:

Pouya Narimani (pouya.narimani@ut.ac.ir).
Hamed Heidari (hamed.h@live.com).

(c) Copyright BCoLab, All Rights Reserved. NO WARRANTY.

"""

import os, sys
import dicom as pydicom
import numpy as np
import time
import mmap
import gdcm
import scipy.ndimage
import copy

# import nibabel as nib


class DicomClass:
    dicomData = []
    dicomDataRaw = []
    dicomDataReslice = []
    isResliceExist = False
    dicomSizePixel = []
    dicom_chamber = []
    pos = []
    ct = []
    ct1 = []
    ct2 = []
    scale = []
    reslice = []
    zeroPos = []
    markerPos = (0, 0, 0)
    markerFlag = False
    dicomClassState = 0

    files = []
    info = []
    inst = []
    ser = []
    idx = []
    instN = []

    # def __init__(self):

    def DicomSelect(self, PathDicom):
        self.files = []  # create an empty list
        for dirName, subdirList, fileList in os.walk(PathDicom):
            for filename in fileList:
                # if ".dcm" in filename.lower():  # check whether the file's DICOM
                #     self.files.append(os.path.join(dirName, filename))
                # else:

                try:
                    pydicom.read_file(os.path.join(dirName, filename))
                    self.files.append(os.path.join(dirName, filename))
                except:
                    time.sleep(0)
                    # nib.load(os.path.join(dirName, filename))
                    # self.files.append(os.path.join(dirName, filename))

        self.inst = ["" for x in range(len(self.files))]
        self.ser = ["" for x in range(len(self.files))]
        self.instN = ["" for x in range(len(self.files))]

        # print(self.ser)

        for i in range(len(self.files)):
            # try:
            self.info = pydicom.read_file(self.files[i])
            # except:
                # self.info = nib.load(self.files[i])


            self.inst[i] = self.info.SOPInstanceUID
            self.ser[i] = self.info.SeriesInstanceUID
            self.instN[i] = self.info.InstanceNumber

        # print(self.ser)


        if (len(self.ser) > 0):
            id, self.idx = np.unique(self.ser, return_inverse=True)
            label = ["" for x in range(len(id))]
            for i in range(len(id)):
                temp = id[i]
                label[i] = ("%02d" % i) + " - (" + str(len(np.where(self.idx == i)[0])) + " Images)" + " Series " + str(
                    temp)

        return label

    def DicomRead(self, id, rsizeFlag=0):
        idx1 = np.where(self.idx == id)[0][0]
        info = pydicom.read_file(self.files[idx1])

        self.scaleM = (float(info.PixelSpacing[0]), float(info.PixelSpacing[1]), float(info.SliceThickness))
        self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
        self.dicomSizePixel = (int(info.Rows), int(info.Columns), len(np.where(self.idx == id)[0]))

        # print('----------------------------------------')
        # print(self.scaleM)
        # print(self.scale)
        # print('----------------------------------------')

        tmp = [i for i in np.nonzero(self.idx == id)]
        temp = ([self.inst[i] for i in np.nonzero(self.idx == id)[0]])
        temp1 = ([self.instN[i] for i in np.nonzero(self.idx == id)[0]])

        inst1 = list(map(str, self.inst))

        try:
            firstDicom = pydicom.read_file(self.files[self.inst.index(temp[0])]).pixel_array
            lastDicom = pydicom.read_file(self.files[self.inst.index(temp[-1])]).pixel_array
            serieLen = len(temp)
            if (firstDicom.shape != lastDicom.shape):
                self.dicomSizePixel = (self.dicomSizePixel[0], self.dicomSizePixel[1], self.dicomSizePixel[2] - 1)
                serieLen = serieLen - 1
            self.ct = np.zeros(self.dicomSizePixel, dtype=firstDicom.dtype)
            for i in range(serieLen):
                self.ct[:, :, i] = pydicom.read_file(self.files[tmp[0][temp1.index(i + 1)]]).pixel_array

        except:
            firstDicom = self.cn(self.files[self.inst.index(temp[0])]).pixel_array
            lastDicom = self.cn(self.files[self.inst.index(temp[0])]).pixel_array
            serieLen = len(temp)
            if (firstDicom.shape != lastDicom.shape):
                self.dicomSizePixel = (self.dicomSizePixel[0], self.dicomSizePixel[1], self.dicomSizePixel[2] - 1)
                serieLen = serieLen - 1
            self.ct = np.zeros(self.dicomSizePixel, dtype=firstDicom.dtype)

            #######################################
            # temp1.sort()
            # for i in range(temp1[0],temp1[-1]+1):
            #     self.ct[:, :, i] = self.cn(self.files[tmp[0][temp1.index(i + 1)]]).pixel_array
            #######################################

            for i in range(len(temp)):
                self.ct[:, :, i] = self.cn(self.files[tmp[0][temp1.index(i + min(temp1))]]).pixel_array

        self.dicomSizeMM = np.array(self.dicomSizePixel) * np.array(self.scaleM)

        # Check Direction
        IOP = info.ImageOrientationPatient
        plane = self.file_plane(IOP)

        if (plane == "Sagittal"):
            # ctxs = ( int(info.Columns), len(np.where(self.idx == id)[0]),int(info.Rows))
            ctxs = (self.ct.shape[1], self.ct.shape[2], self.ct.shape[0])
            ctx = np.zeros(ctxs, dtype=firstDicom.dtype)
            for i in range(self.ct.shape[0]):
                ctx[:, :, i] = self.ct[i, :, :]
            self.ct = np.rot90(np.rot90(ctx, axes=(0, 2)), axes=(0, 2))
            # self.scaleM = ( float(info.PixelSpacing[1]), float(info.SliceThickness),float(info.PixelSpacing[0]))
            self.scaleM = (self.scaleM[1], self.scaleM[2], self.scaleM[0])
            self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
            self.dicomSizePixel = (self.dicomSizePixel[1], self.dicomSizePixel[2], self.dicomSizePixel[0])
            self.dicomSizeMM = np.array(self.dicomSizePixel) * np.array(self.scaleM)

        # aaaa=self.resize()

        if rsizeFlag:
            self.ResizeDicom()

        self.ct1 = np.uint8(np.round(self.ct / self.ct.max() * 255))
        self.dicomDataRaw = copy.deepcopy(self.ct1)
        # self.ct2 = self.ct / self.ct.max()
        self.dicomData = self.ct1

    def DicomRead1(self, fn, rsizeFlag):
        info = pydicom.read_file(fn)

        self.scaleM = (float(info.PixelSpacing[0]), float(info.PixelSpacing[1]), float(info.SliceThickness))
        self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
        self.dicomSizePixel = (int(info.Rows), int(info.Columns), info.NumberofFrames)
        self.dicomSizeMM = np.array(self.dicomSizePixel) * np.array(self.scaleM)
        tmp = [i for i in np.nonzero(self.idx == id)]
        temp = ([self.inst[i] for i in np.nonzero(self.idx == id)[0]])
        temp1 = ([self.instN[i] for i in np.nonzero(self.idx == id)[0]])

        inst1 = list(map(str, self.inst))

        # self.ct=info.pixel_array
        self.ct = np.zeros((self.dicomSizePixel))

        for i in range(self.dicomSizePixel[2]):
            self.ct[:, :, i] = info.pixel_array[i, :, :]

        if rsizeFlag:
            self.ResizeDicom()
        # Check Direction
        # IOP = info.ImageOrientationPatient
        # plane = self.file_plane(IOP)
        # if (plane=="Sagittal"):
        #     ctxs = ( int(info.Columns), len(np.where(self.idx == id)[0]),int(info.Rows))
        #     ctx=  np.zeros(ctxs, dtype=np.uint16)
        #     for i in range(self.ct.shape[0]):
        #            ctx[:, :, i]=self.ct[i, :, :]
        #     self.ct = np.rot90(np.rot90(ctx,axes=(0,2)),axes=(0,2))
        #     self.scaleM = ( float(info.PixelSpacing[1]), float(info.SliceThickness),float(info.PixelSpacing[0]))
        #     self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
        #     self.dicomSizePixel = ( int(info.Columns), len(np.where(self.idx == id)[0]),int(info.Rows))
        #     self.dicomSizeMM = np.array(self.dicomSizePixel) * np.array(self.scaleM)

        # aaaa=self.resize()
        self.ct1 = np.uint8(np.round(self.ct / self.ct.max() * 255))
        self.dicomDataRaw = np.uint8(np.round(self.ct / self.ct.max() * 255))
        self.ct2 = self.ct / self.ct.max()
        self.dicomData = self.ct1

    def resize(self):
        a = 1.0
        z = np.zeros((np.round(self.dicomSizeMM[0] / a).astype(int), np.round(self.dicomSizeMM[1] / a).astype(int),
                      self.dicomSizePixel[2]))
        zs = z.shape

        for i in range(self.ct.shape[2]):
            tmp1 = self.ct[:, :, i]
            tmp2 = scipy.misc.imresize(tmp1, (zs[0], zs[1]))
            z[:, :, i] = tmp2
        self.ct = z

        z = np.zeros((np.round(self.dicomSizeMM[0] / a).astype(int), np.round(self.dicomSizeMM[1] / a).astype(int),
                      np.round(self.dicomSizeMM[2] / a).astype(int)))
        zs = z.shape
        for i in range(self.ct.shape[0]):
            tmp1 = self.ct[i, :, :]
            tmp2 = scipy.misc.imresize(tmp1, (zs[1], zs[2]))
            z[i, :, :] = tmp2
        self.ct = z

        self.scale = (1.0, 1.0, 1.0)
        self.scaleM = (a, a, a)
        self.dicomSizePixel = zs
        return z

    def resize1(self):
        if self.scale[0] != 1.0:
            z = np.zeros((np.round(self.dicomSizePixel[0] * self.scale[0]).astype(int), self.dicomSizePixel[1],
                          self.dicomSizePixel[2]))
            for i in range(self.ct.shape[2]):
                tmp1 = self.ct[:, :, i]
                tmp2 = scipy.misc.imresize(tmp1, (
                np.round(self.dicomSizePixel[0] * self.scale[0]).astype(int), self.dicomSizePixel[1]))
                z[:, :, i] = tmp2
            self.ct = z
        if self.scale[1] != 1.0:
            z = np.zeros((self.dicomSizePixel[0], np.round(self.dicomSizePixel[1] * self.scale[1]).astype(int),
                          self.dicomSizePixel[2]))
            for i in range(self.ct.shape[2]):
                tmp1 = self.ct[:, :, i]
                tmp2 = scipy.misc.imresize(tmp1, (
                self.dicomSizePixel[0], np.round(self.dicomSizePixel[1] * self.scale[1]).astype(int)))
                z[:, :, i] = tmp2
            self.ct = z
        if self.scale[2] != 1.0:
            z = np.zeros((self.dicomSizePixel[0], self.dicomSizePixel[1],
                          np.round(self.dicomSizePixel[2] * self.scale[2]).astype(int)))
            for i in range(self.ct.shape[0]):
                tmp1 = self.ct[i, :, :]
                tmp2 = scipy.misc.imresize(tmp1, (
                self.dicomSizePixel[1], np.round(self.dicomSizePixel[2] * self.scale[2]).astype(int)))
                z[i, :, :] = tmp2
            self.ct = z

        self.scale = (1.0, 1.0, 1.0)

        return z

    def cn(self, file1):
        file2 = "tmp00.dcm"  # output filename

        reader = gdcm.ImageReader()
        reader.SetFileName(file1)
        reader.Read()
        change = gdcm.ImageChangeTransferSyntax()
        change.SetTransferSyntax(gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian))
        change.SetInput(reader.GetImage())
        change.Change()
        writer = gdcm.ImageWriter()
        writer.SetFileName(file2)
        writer.SetFile(reader.GetFile())
        writer.SetImage(change.GetOutput())
        writer.Write()
        zz = pydicom.read_file("tmp00.dcm")
        os.remove("tmp00.dcm")
        return zz

    def file_plane(self, IOP):
        IOP_round = [round(x) for x in IOP]
        plane = np.cross(IOP_round[0:3], IOP_round[3:6])
        plane = [abs(x) for x in plane]
        if plane[0] == 1:
            return "Sagittal"
        elif plane[1] == 1:
            return "Coronal"
        elif plane[2] == 1:
            return "Transverse"

    def ResizeDicom(self):
        # newScaleM=(0.5,0.5,0.5)
        newScaleM = (1.0, 1.0, 1.0)
        # z = np.zeros((np.round(self.dicomSizePixel[0] * self.scaleM[0]/newScaleM[0]).astype(int),
        #              np.round(self.dicomSizePixel[1] * self.scaleM[1]/newScaleM[1]).astype(int),
        #              np.round(self.dicomSizePixel[2] * self.scaleM[2]/newScaleM[2]).astype(int)))
        z1 = np.zeros((np.round(self.dicomSizePixel[0] * self.scaleM[0] / newScaleM[0]).astype(int),
                       np.round(self.dicomSizePixel[1] * self.scaleM[1] / newScaleM[1]).astype(int),
                       self.dicomSizePixel[2]))
        z2 = np.zeros((np.round(self.dicomSizePixel[0] * self.scaleM[0] / newScaleM[0]).astype(int),
                       np.round(self.dicomSizePixel[1] * self.scaleM[1] / newScaleM[1]).astype(int),
                       np.round(self.dicomSizePixel[2] * self.scaleM[2] / newScaleM[2]).astype(int)))

        if ((self.scaleM[0] != newScaleM[0]) or (self.scaleM[1] != newScaleM[1])):
            for i in range(self.ct.shape[2]):
                tmp1 = self.ct[:, :, i]
                tmp1[tmp1 < 20] = 0
                tmp2 = scipy.misc.imresize(tmp1,
                                           (
                                           np.round(self.dicomSizePixel[0] * self.scaleM[0] / newScaleM[0]).astype(int),
                                           np.round(self.dicomSizePixel[1] * self.scaleM[1] / newScaleM[1]).astype(
                                               int)))
                z1[:, :, i] = tmp2
            self.dicomSizePixel = (np.round(self.dicomSizePixel[0] * self.scaleM[0] / newScaleM[0]).astype(int),
                                   np.round(self.dicomSizePixel[1] * self.scaleM[1] / newScaleM[1]).astype(int),
                                   self.dicomSizePixel[2])
            self.scaleM = (newScaleM[0], newScaleM[1], self.scaleM[2])
            zz = z1

        if (self.scaleM[2] != newScaleM[2]):
            for i in range(zz.shape[0]):
                tmp1 = zz[i, :, :]
                tmp1[tmp1 < 20] = 0
                tmp2 = scipy.misc.imresize(tmp1, (self.dicomSizePixel[1],
                                                  np.round(
                                                      self.dicomSizePixel[2] * self.scaleM[2] / newScaleM[2]).astype(
                                                      int)))
                z2[i, :, :] = tmp2
            self.dicomSizePixel = (self.dicomSizePixel[0],
                                   self.dicomSizePixel[1],
                                   np.round(self.dicomSizePixel[2] * self.scaleM[2] / newScaleM[2]).astype(int))
            zz = z2

        self.ct = zz

        self.scaleM = newScaleM
        self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
        self.ct1 = np.uint8(np.round(self.ct / self.ct.max() * 255))
        # self.dicomB.ct1[self.dicomB.ct1<84]=0
        self.dicomData = self.ct1
