import os
import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for

from EcgProcessingService import EcgProcessingService
from EmrCommunicationService import EmrCommunicationService

ImagePath = os.path.join('/static', 'reports')

# Functions
def getDbConnection():
    conn = sqlite3.connect('sql/ecgai.db')
    conn.row_factory = sqlite3.Row
    return conn

def getAllReports():
    conn = getDbConnection()
    reports = conn.execute('SELECT * FROM reports').fetchall()
    conn.close()
    return reports

def getReportsForPatient(patientId):
    conn = getDbConnection()
    reports = conn.execute('SELECT * FROM reports WHERE patientId = ?',
                        (patientId,)).fetchall()
    conn.close()
    return reports

# Endpoints
ecgApi = Flask(__name__)

if __name__ == '__main__':
    ecgApi.run(debug=True)

@ecgApi.route('/')
def index():
    reportsFromDb = getAllReports()
    return render_template(
        'index.html',
        reports = reportsFromDb)

@ecgApi.route('/reports/<int:patientId>')
def reportsForPatient(patientId):
    reportsFromDb = getReportsForPatient(patientId)
    return render_template(
        'report.html', 
        patientId = patientId,
        reports = reportsFromDb,
        imageFilePath = ImagePath)

@ecgApi.route('/process', methods=('GET', 'POST'))
def process():
    if request.method == 'POST':             
        contentType = request.headers.get('Content-Type')
        if (contentType == 'application/json'):
            data = json.loads(request.data)
            patientId = data['patientId']
            examId = data['examId']
            
            emrCommunicationService = EmrCommunicationService() 
            patient = emrCommunicationService.getPatientInfo(patientId)
            exam = emrCommunicationService.getExamInfo(examId)

            ecgProcessingService = EcgProcessingService() 
            aiReport = ecgProcessingService.processAi("output01.png")
            error = ecgProcessingService.createHL7CDA(aiReport)
            error = ecgProcessingService.createDICOMSecondaryCapture(aiReport)
            error = ecgProcessingService.createDICOMStructuredReport(aiReport)

            error = emrCommunicationService.sendHL7CDA("HL7CDA_ECG.xml.base64.JSON.txt")
            error = emrCommunicationService.sendDICOM("output01.png.dcm")
    else:
        return redirect(url_for('index'))
    return render_template(
        'process.html',
        inputImage = "output01.png")
