import csv
import os
import re

import xlrd

# Data Folder Path
data_root = "../rawData/"
nlsy_dict_path = data_root + "NLSY97/NLSY97_Public/"


def extract_nlsy_question():
    with open('output/nlsy_question.tsv', 'wb') as output_file:
        output_writer = csv.writer(output_file, delimiter="\t")
        # iterate over cdb files
        for subdir, dir, files in os.walk(nlsy_dict_path):
            for file in files:
                if file.endswith("cdb"):
                    print file
                    file_path = os.path.join(subdir, file)
                    cdb_file = open(file_path, "r")
                    line = " "
                    variable = ""
                    question = ""
                    while line != "":
                        line = cdb_file.readline()
                        if line.find("Survey Year: ") != -1:
                            variable = line.split(" ")[0].replace(".", "")
                        if line.strip().find("PRIMARY VARIABLE") != -1:
                            cdb_file.readline()
                            cdb_file.readline()

                            question = cdb_file.readline().strip()
                            output = [variable, question.replace(u'\u2018', "'").replace(u'\u2019',"'")]
                            output_writer.writerow(output)
                            print output

if __name__ == '__main__':
    extract_nlsy_question()
