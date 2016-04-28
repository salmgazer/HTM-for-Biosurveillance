    #This is the main client of the system

import csv
import datetime
import os

from model_params.diseases.disease_record_model_params import MODEL_PARAMS
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
import nupic_anomaly_output

mind_palaces = "/home/salifu/Documents/Experiment/examples/opf/clients/ashesi-cs-mhealth/mhealth/MateNeocortex/Disease Outbreak Detection/mind_palaces/"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def createModel():
    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({
        "predictedField": "disease_name"
    })
    return model

def runModel(model, inputFilePath):
    inputFile = open(inputFilePath, "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()
    csvReader.next()
    csvReader.next()

    output = nupic_anomaly_output.NuPICFileOutput("disease_forecast")

    shifter = InferenceShifter()
    counter = 0
    actualCount = 0
    predictCount = 0
    miss = 0
    hit = 0
    row_count = 0
    for row in csvReader:
        if row_count > 1000:
            break
        counter += 1
        if(counter % 10 == 0):
            print "Read %i lines..." % counter
        disease_date = datetime.datetime.strptime(row[5], DATE_FORMAT)
        disease_name = str(row[2])
        result = model.run({
            "disease_name": disease_name,
            "disease_date": disease_date
        })

        result = shifter.shift(result)
        prediction = str(result.inferences["multiStepBestPredictions"][20])
        anomalyScore = int(result.inferences["anomalyScore"])

        output.write(disease_date, disease_name, prediction, anomalyScore)
        if prediction == "Malaria":
            predictCount += 1
        if disease_name == "Malaria" and prediction != None:
            actualCount += 1
        if prediction != None:
            if disease_name == prediction:
                hit += 1
            else:
                miss += 1
        row_count += 1
        print counter, row[0], "Actual: ", disease_name, "Predicted: ", prediction, "------", anomalyScore
    print"\n Number of actuals: ", actualCount," \n Number of predictions: ", predictCount
    print "\n hits: ", hit,"\n misses: ", miss-20

def model_exists(model_path):
    if os.path.isfile(model_path):
        return True
    else:
        return False

def runHospitalModel(inputFilePath):
    model = None
    if model_exists(mind_palaces+"disease20_com17"+"/model.pkl"):
        print "using existing model"
        model = ModelFactory.loadFromCheckpoint(mind_palaces+"disease20_com17")
    else:
        print "creating new model"
        model = createModel()
    runModel(model, inputFilePath)
    print "======> updating model"
    model.save(mind_palaces+"disease20_com17")


if __name__ == "__main__":
    inputFilePath = "positive_community17.csv"
    for i in range(1):
        print "========================= ", i, " ============================="
        runHospitalModel(inputFilePath)
