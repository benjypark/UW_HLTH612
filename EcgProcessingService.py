import struct
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian
import pydicom._storage_sopclass_uids

import numpy as np

from PIL import Image

class AiReport():
    def __init__(self, ClassName, PredictionScore, HeatmapImage):
        self.ClassName = ClassName
        self.PredictionScore = PredictionScore
        self.HeatmapImage = HeatmapImage    

class EcgProcessingService():
    
    def processAi(self, originalEcgImage):
        #
        # Run AI algorithms
        #

        print("========== AI ECG Start Processing ==========\n")
        
        aiReport = AiReport("ARVC", "0.9501", "output01.png")

        print("========== AI ECG Prediction Result ==========")
        print("== Class: " + aiReport.ClassName)
        print("== Prediction Score: " + aiReport.PredictionScore)
        print("== Heatmap Image: " + aiReport.HeatmapImage)
        print(" ")

        return aiReport

    def createHL7CDA(self, aiReport):
        #
        # Create HL7 CDA Document
        #

        print("========== Generate HL7 CDA Document ==========")

        return 1

    def createDICOMSecondaryCapture(self, aiReport):
        #
        # Create DICOM Secondary Capture
        #

        print("========== Generate DICOM Image : " + aiReport.HeatmapImage + "==========")

        meta = FileMetaDataset()
        meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.SecondaryCaptureImageStorage
        meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  
        
        ds = Dataset()
        ds.file_meta = meta
        ds.is_little_endian = True
        ds.is_implicit_VR = False
        ds.SOPClassUID = pydicom._storage_sopclass_uids.SecondaryCaptureImageStorage
        ds.PatientName = "Patient^Name"
        ds.PatientID = "12345678"
        ds.Modality = "OT"
        ds.SeriesInstanceUID = pydicom.uid.generate_uid()
        ds.StudyInstanceUID = pydicom.uid.generate_uid()
        
        originalImage = Image.open(aiReport.HeatmapImage)
        numpyImage = np.array(originalImage.getdata(), dtype=np.uint8)[:,:3]
        ds.Rows = originalImage.height
        ds.Columns = originalImage.width
        ds.PhotometricInterpretation = "RGB"
        ds.SamplesPerPixel = 3
        ds.BitsStored = 8
        ds.BitsAllocated = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.PixelData = numpyImage.tobytes()
        ds.save_as(aiReport.HeatmapImage + ".dcm")

        return 1

    def createDICOMStructuredReport(self, aiReport):
        #
        # Create DICOM Structured Report
        #

        print("========== Generate DICOM Structured Report : " + aiReport.HeatmapImage + "==========")

        return 1
