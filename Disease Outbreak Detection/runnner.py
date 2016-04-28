    #This is the main client of the system

import csv
import datetime
import os

from model_params.weight.weight_record_model_params import MODEL_PARAMS
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
import nupic_anomaly_output

mind_palaces = "/home/salifu/Documents/Experiment/examples/opf/clients/ashesi-cs-mhealth/mhealth/MateNeocortex/Disease Outbreak Detection/mind_palaces/"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def createModel():
    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({
        "predictedField": "weight"
    })
    return model

def runModel(model, inputFilePath):
    inputFile = open(inputFilePath, "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()
    csvReader.next()
    csvReader.next()

    output = nupic_anomaly_output.NuPICFileOutput("weight_output")

    shifter = InferenceShifter()
    counter = 0

    for row in csvReader:
        counter += 1
        if(counter % 20 == 0):
            print "Read %i lines..." % counter
        weight_date = datetime.datetime.strptime("2013-01-08 12:00:00", DATE_FORMAT)
        weight = row[2]
        result = model.run({
            "weight": weight,
            "weight_date": weight_date
        })

        result = shifter.shift(result)
        prediction = str(result.inferences["multiStepBestPredictions"][1])
        anomalyScore = int(result.inferences["anomalyScore"])

        output.write(weight_date, weight, prediction, anomalyScore)

def model_exists(model_path):
    if os.path.isfile(model_path):
        return True
    else:
        return False

def runHospitalModel(inputFilePath):
    model = None
    if model_exists(mind_palaces+"weight"+"/model.pkl"):
        print "using existing model"
        model = ModelFactory.loadFromCheckpoint(mind_palaces+"weight")
    else:
        print "creating new model"
        model = createModel()
    runModel(model, inputFilePath)
    print "======> updating model"
    model.save(mind_palaces+"weight")


if __name__ == "__main__":
    inputFilePath = "patients_kassena.csv"
    for i in range(1):
        print "========================= ", i, " ============================="
        runHospitalModel(inputFilePath)
