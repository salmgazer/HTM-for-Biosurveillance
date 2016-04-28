import sys
import csv
import operator


def sortByDate(filename, output_filename):
	# output
	output_file = csv.writer(open(output_filename, "w"), delimiter=",") 
	# input file
	reader = csv.reader(open(filename, "r"), delimiter=",")
	# sort data by date
	sortedlist = sorted(reader, key=operator.itemgetter(5), reverse=False)

	# write sorted list to new file
	for a_row in sortedlist:
		output_file.writerow(a_row)

def sortByLocation(filename, output_filename):
	# output
	output_file = csv.writer(open(output_filename, "w"), delimiter=",")
	# input file
	reader = csv.reader(open(filename, "r"), delimiter=",")
	#sort data by location
	sortedlist = sorted(reader, key=operator.itemgetter(4), reverse=False)

	# write sorted list to new file
	for a_row in sortedlist:
		output_file.writerow(a_row)

def getByLocation(location, output_filename, filename):
	# output
	output_file = csv.writer(open(output_filename, "w"), delimiter=",")
	# input file
	reader = csv.reader(open(filename, "r"), delimiter=",")

	# get all rows from community
	for a_row in reader:
		if a_row[3] == location:
			output_file.writerow(a_row)

def frequency(filename):
	reader = csv.reader(open(filename, "r"), delimiter=",")

	malaria = 0
	ari = 0
	for a_row in reader:
		if a_row[2] == "Malaria":
			malaria += 1
		elif a_row[2] == "ARI":
			ari += 1
	print "Malaria count is :: ", malaria
	print "ARI count is :: ", ari 

def getAllLocationsData(filename):
	locations = []
	# output
	# output_file = open(output_filename,"w")
	# input file
	reader = csv.reader(open(filename, "r"), delimiter=",")

	# store locations in list
	for a_row in reader:
		if a_row[4] not in locations and a_row[4] != "location":
			locations.append(a_row[4])
	# write number of communities to file
	# output_file.write(str(len(locations))+"\n")
	# write locations to file
	# for a_loc in locations:
	# 	output_file.write(a_loc+"\n")
	community_count = 1
	for a_loc in locations:
		com_file_name = "community"+str(community_count)+".csv"
		community_data = csv.writer(open(com_file_name, "w"), delimiter=",")
		community_data.writerow(['patient_id', 'record_id', 'reported_case', 'outcome', 'location', 'date'])
		reader = csv.reader(open(filename, "r"), delimiter=",")
		row_count = 0
		for a_row in reader:
			if a_row[4] == a_loc:
				community_data.writerow(a_row)
				row_count += 1
		community_count += 1
		print com_file_name,"  ::  ",row_count

def getAllPositiveOutcomes(filename):
	# input file
	reader = csv.reader(open(filename, "r"), delimiter=",")

	output_file = csv.writer(open("positive_"+filename, "w"), delimiter=",")
	reader.next()
	output_file.writerow(['patient_id', 'record_id', 'disease_name', 'outcome', 'location', 'date'])
	for a_row in reader:
		if int(a_row[3]) == 0:
			continue
		output_file.writerow(a_row)

def compV_B(filename):
    reader = csv.reader(open(filename, "r"), delimiter=",")
    bcg_count = 0
    vitA_count = 0
    for a_row in reader:
        # print "current is ", a_row[1]
        if a_row[1] == "BCG":
            bcg_count += 1
        elif a_row[1] == "Vitamin A (6month)":
            vitA_count += 1
    print "Vitamin A (6month)  :  ", vitA_count
    print "BCG                 :  ", bcg_count 
            


if __name__ == '__main__':
    compV_B("vaccine_record1.csv")
	# sortByDate("reported_cases.csv", "clean_reported_cases_by_date.csv")
	# sortByLocation("clean_reported_cases_by_date.csv", "clean_reported_cases.csv")
	# getAllLocationsData("clean_reported_cases.csv")
	# getAllPositiveOutcomes("community19.csv")
	# getByLocation("Kassena-Nankana West", "patients_kassena.csv", "patient_info.csv")
