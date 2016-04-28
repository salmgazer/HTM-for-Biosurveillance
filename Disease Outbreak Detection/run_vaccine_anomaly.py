    #This is the main client of the system

import csv
import datetime
import os

from model_params.vaccination.vaccine_record_model_params import MODEL_PARAMS
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory
import nupic_anomaly_output
# from nupic.algorithms import anomaly_likelihood


mind_palaces = "/home/salifu/Documents/Experiment/examples/opf/clients/ashesi-cs-mhealth/mhealth/MateNeocortex/Disease Outbreak Detection/mind_palaces/"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def createModel():
    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({
        "predictedField": "vaccine_name"
    })
    return model

def runModel(model, inputFilePath, run_count):
    inputFile = open(inputFilePath, "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()
    csvReader.next()
    csvReader.next()

    output = nupic_anomaly_output.NuPICFileOutput("Vaccination_present")

    shifter = InferenceShifter()
    counter = 0
    actualCount = 0
    predictCount = 0
    miss = 0
    hit = 0
    vaccine_actuals = {}
    vaccine_predictions = {}

    # accuracy_file = open("vaccine_accuracy.txt", "w")
    com_file_name = "vaccination_accuracy_present.csv"
    accuracy_dir = "vaccine_accuracy_dir/"
    vaccine_accuracy = csv.writer(open(accuracy_dir+com_file_name, "a"), delimiter=",")
    vaccine_accuracy.writerow(['Run number '+str(run_count)])

    for row in csvReader:
        counter += 1
        if(counter % 20 == 0):
            # start miss and hit counts
            miss = 0
            hit = 0
            file_row = []
            ## writing to file
            # file_line = "==============================\n"
            # for key, value in vaccine_actuals.iteritems():
                # file_line += key+" : "+str(value)+"   "+str(vaccine_predictions.get(key, 0))+"\n"
            for key in vaccine_actuals:
                if vaccine_actuals[key] != None:
                    file_row.append(str(vaccine_actuals[key]))
                else:
                    file_row.append(str(0))
                if vaccine_predictions.get(key) != None:
                    file_row.append(str(vaccine_predictions.get(key)))
                else:
                    file_row.append(str(0))
                # vaccine_accuracy.writerow([key, str(value), str(vaccine_predictions.get(key, 0))])
            vaccine_accuracy.writerow(file_row)
            # write line to file
            #accuracy_file.write(file_line)
            file_row = []
            for key in vaccine_actuals:
                vaccine_actuals[key] = 0
            for key in vaccine_predictions:
                vaccine_predictions[key] = 0
            print "Read %i lines..." % counter
        vaccine_date = datetime.datetime.strptime(row[2], DATE_FORMAT)
        vaccine_name = str(row[1])
        result = model.run({
            "vaccine_date": vaccine_date,
            "vaccine_name": vaccine_name
        })

        result = shifter.shift(result)
        prediction = str(result.inferences["multiStepBestPredictions"][20])
        anomalyScore = int(result.inferences["anomalyScore"])
        # abnormal = anomaly_likelihood.AnomalyLikelihood()
        """anomalyLikelihood = abnormal.anomalyProbability(
            vaccine_name, anomalyScore, vaccine_date
        )"""

        output.write(vaccine_date, vaccine_name, prediction, anomalyScore)
         # if vaccine not in actuals
        if vaccine_actuals.get(vaccine_name) == None:
            # print "got you now", vaccine_name
            vaccine_actuals.update({vaccine_name: 1})
            # update value if actual already exitsts
        else:
            vaccine_actuals[vaccine_name] += 1
        # if vaccine not in predictions
        if vaccine_predictions.get(prediction) == None:
            vaccine_predictions.update({prediction: 1})
            # update value if prediction alreadye exists
        else:
            vaccine_predictions[prediction] += 1
        if prediction == vaccine_name:
            hit += 1
        else:
            miss += 1
        """print counter, "community member_id: ", row[0], "Actual: ", vaccine_name, "Predicted: ", prediction, "------", anomalyScore, "====>> ", anomalyLikelihood"""
        print counter, "Actual: ", vaccine_name, "Predicted: ", prediction, " =====        ", anomalyScore
        if anomalyScore == 1:
            print "**************************"
            print "**************************"
            print "**************************"
            print "****                  ****"
            print "****                  ****"
            print "****                  ****"
            print "**** ",vaccine_name," ****"
            print "****                  ****"
            print "****                  ****"
            print "****                  ****"
            print "**************************"
            print "**************************"
            print "**************************"
            
    # close accuracy file
    #accuracy_file.close()
    print"\n Number of actuals: ", actualCount," \n Number of predictions: ", predictCount
    print "\n hits: ", hit,"\n misses: ", miss
    print "List of actuals"
    print vaccine_actuals
    print "List of predictions"
    print vaccine_predictions

def model_exists(model_path):
    if os.path.isfile(model_path):
        return True
    else:
        return False

def runHospitalModel(inputFilePath, run_count):
    model = None
    if model_exists(mind_palaces+"vaccination_present"+"/model.pkl"):
        print "using existing model"
        model = ModelFactory.loadFromCheckpoint(mind_palaces+"vaccination_present")
    else:
        print "creating new model"
        model = createModel()
    runModel(model, inputFilePath, run_count)
    print "======> updating model"
    model.save(mind_palaces+"vaccination_present")


if __name__ == "__main__":
    inputFilePath = "vaccine_record_short_anomaly.csv"
    for i in range(5):
        print "========================= ", i+1, " ============================"
        runHospitalModel(inputFilePath, i+1)
