import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import os, sys
# import dicom as pydicom
# import numpy as np
import time
import mmap
# import gdcm
# import scipy.ndimage
import copy


class NiftiClass:
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

    def DicomSelect(self, PathDicom):
        self.files = []  # create an empty list
        for dirName, subdirList, fileList in os.walk(PathDicom):
            for filename in fileList:
                # if ".dcm" in filename.lower():  # check whether the file's DICOM
                #     self.files.append(os.path.join(dirName, filename))
                # else:

                try:
                    nib.load(os.path.join(dirName, filename))
                    self.files.append(os.path.join(dirName, filename))
                	# nib.load(os.path.join(dirName, filename))
                    # pydicom.read_file(os.path.join(dirName, filename))
                    # self.files.append(os.path.join(dirName, filename))
                except:
                    time.sleep(0)


        # self.inst = ["" for x in range(len(self.files))]
        # self.ser = ["" for x in range(len(self.files))]
        # self.instN = ["" for x in range(len(self.files))]

        for i in range(len(self.files)):
            # try:
            #     self.info = pydicom.read_file(self.files[i])
            # except:
            self.info = nib.load(self.files[i])


            # self.inst[i] = self.info.SOPInstanceUID
            # self.ser[i] = self.info.SeriesInstanceUID
            # self.instN[i] = self.info.InstanceNumber


        # if (len(self.ser) > 0):
        #     id, self.idx = np.unique(self.ser, return_inverse=True)
        #     label = ["" for x in range(len(id))]
        #     for i in range(len(id)):
        #         temp = id[i]
        #         label[i] = ("%02d" % i) + " - (" + str(len(np.where(self.idx == i)[0])) + " Images)" + " Series " + str(
        #             temp)

        # label = []
        # for i in range(len(self.files)):
        #     label.append(self.fi)



        return self.files


    def DicomRead(self, id, rsizeFlag=0):
        img = nib.load(id)
        header = img.header

        self.ct = np.array(img.get_data())
        # plt.imshow(self.ct[0], cmap='gray')
        # plt.show()
        # print(self.ct.min(), self.ct.max())
        # print('---------------------------------')
        self.ct1 = np.uint8(((self.ct - self.ct.min()) / (self.ct.max() - self.ct.min())) * 255)

        # plt.imshow(self.ct[0], cmap='gray')
        # plt.show()
        # print(self.ct1.min(), self.ct1.max())

        self.dicomData = self.ct1

        self.dicomSizePixel = header.get_data_shape()

        self.scaleM = header.get_zooms()[:3]
        self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
        self.dicomSizeMM = np.array(self.dicomSizePixel) * np.array(self.scaleM)
        # self.scaleM = (float(info.PixelSpacing[0]), float(info.PixelSpacing[1]), float(info.SliceThickness))
        


        '''
        idx1 = np.where(self.idx == id)[0][0]
        info = pydicom.read_file(self.files[idx1])

        self.scaleM = (float(info.PixelSpacing[0]), float(info.PixelSpacing[1]), float(info.SliceThickness))
        self.scale = tuple(x / min(self.scaleM) for x in self.scaleM)
        self.dicomSizePixel = (int(info.Rows), int(info.Columns), len(np.where(self.idx == id)[0]))

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
        '''

        # self.dicomData = np.array(img.get_data())