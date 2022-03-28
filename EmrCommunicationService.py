import requests
import json

class EmrCommunicationService():
    
    def getPatientInfo(self, patientId):
        #
        # Get Patient Info from EMR
        #

        response = requests.get("http://10.0.0.102:8080/fhir/Patient/" + patientId)        
        print("========== Get Patient Info from EMR: " + patientId + " ==========")
        pretty_json = json.loads(response.text)
        print(json.dumps(pretty_json, indent=4), flush=True)

        return 1

    def getExamInfo(self, examId):
        #
        # Get Exam Info from EMR
        #

        response = requests.get("http://10.0.0.102:8080/fhir/Observation/"+ examId)
        print("========== Get Exam Info from EMR: " + examId + " ==========")
        pretty_json = json.loads(response.text)
        print(json.dumps(pretty_json, indent=4), flush=True)

        return 1

    def sendHL7CDA(self, cda):
        #
        # Send HL7 CDA to EMR
        #
        
        print("========== Send CDA to EMR ==========")
        print("== Sending ... " + cda)

        header = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        cdaFile = open(cda, "r")
        contents = cdaFile.read()
        response = requests.put("http://10.0.0.102:8080/fhir/DocumentReference", contents, headers = header)
        print(response, flush=True)

        return 1

    def sendDICOM(self, dicom):
        #
        # Send DICOM to PACS
        #

        print("========== Send DICOM to PACS ==========")
        print("== Sending ... " + dicom)

        return 1