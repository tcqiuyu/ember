import numpy as np
import os
import csv
import logging
import pickle

training_data_path_base = "../../../data/training/"
training_matrix = []


def preprocess_training_data(name):
    if name is "msr":
        path = training_data_path_base + "paraphrase_corpus"
        matrix = []
        for subdir, dir, files in os.walk(path):
            for file in files:
                file = os.path.join(subdir, file)
                if file.endswith("tsv"):
                    with open(file, mode='r') as csvfile:
                        logging.info("Parsing " + file)
                        rows = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
                        next(rows, None)
                        for row in rows:
                            matrix.append([[row[3], row[4]], row[0]])
        training_matrix.extend(matrix)

    elif name is "sick":
        path = training_data_path_base + "sick"
        matrix = []
        for subdir, dir, files in os.walk(path):
            for file in files:
                file = os.path.join(subdir, file)
                if file.endswith("txt"):
                    with open(file, mode='r') as csvfile:
                        logging.info("Parsing " + file)
                        rows = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
                        next(rows, None)
                        for row in rows:
                            score = float(row[3]) / 5
                            matrix.append([[row[1], row[2]], score])
        training_matrix.extend(matrix)

    elif name is "sts":
        path = training_data_path_base + "STS/2016"
        matrix = []
        for subdir, dir, files in os.walk(path):
            for file in files:
                file = os.path.join(subdir, file)
                if file.endswith("tsv"):
                    with open(file, mode='r') as csvfile:
                        logging.info("Parsing " + file)
                        rows = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
                        next(rows, None)
                        for row in rows:
                            if row[0] != "":
                                score = float(row[0]) / 5
                                matrix.append([[row[1], row[2]], score])
        training_matrix.extend(matrix)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(asctime)s %(filename)s[line:%(lineno)d] %(message)s")

    preprocess_training_data('msr')
    preprocess_training_data('sick')
    preprocess_training_data('sts')

    f = open(training_data_path_base + "training_data.pickle", "wb")
    pickle.dump(training_matrix, f)
    f.close()
    # joblib.dump(training_matrix, training_data_path_base + "training_data.matrix")
