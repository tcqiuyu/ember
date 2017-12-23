import csv
import json
import os

from pymongo import MongoClient

data_root = "../rawData"
data_format = {"Add Health": ".tab", "NEXT": ".CSV", "NLSY97": ".csv"}
data_metadata_format = {"Add Health": ".xls", "NEXT": ".csv", "NLSY97": ".dct"}
data_id = {"Add Health": "AID", "NEXT": "StudyID", "NLSY97": "R0000100"}

from utils import *
from pymongo.errors import DuplicateKeyError

server = startServer()

try:
    client = MongoClient(local_bind_ip, server.local_bind_port)
    print client.server_info()

    for dataset in data_format.keys():
        directory = data_root + "/" + dataset
        print dataset
        db = client[dataset.replace(" ", "_")]
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(data_format.get(dataset)):

                    print "\t" + subdir
                    file_path = os.path.join(subdir, file)
                    data_file = open(file_path)
                    if dataset == "Add Health":
                        collection_name = subdir.split("\\")[-1].split("_")[0].strip(" ") + "_" + \
                                          subdir.split("_")[-1].strip(" ")
                        data_reader = csv.reader(data_file, dialect=tsv)
                    elif dataset == "NLSY97" or dataset == "NEXT":
                        collection_name = file.split(".")[0]
                        data_reader = csv.reader(data_file)
                    print "\t" + collection_name
                    print "\t\t" + file
                    data_header = data_reader.next()
                    idx = 1

                    collection = db[collection_name]

                    while True:
                        try:
                            current_line = data_reader.next()
                            json_current_line = convert_csv_to_json(current_line, data_header,
                                                                    id_header=data_id.get(dataset))
                            collection.insert_one(json.loads(json_current_line))
                            if idx % 100 == 0:
                                print (
                                    "=== %d Documents are inserted to \"%s\" in db \"%s\" ===" % (
                                        idx, collection_name, dataset))
                            idx = idx + 1
                        except DuplicateKeyError as e:
                            # print e
                            idx = idx + 1
                            continue
                        except csv.Error as e:
                            print "Error parsing file %s: %s" % (file_path, e)
                        except ValueError as e:
                            log_file = open("log/value_error." + dataset + "." + collection_name + ".log", "w")
                            log_file.write(str(current_line))
                            log_file.write("\n")
                            log_file.write(str(e.message))
                            log_file.write("\n")
                            continue
                        except IndexError as e:
                            log_file = open("log/index_error." + dataset + "." + collection_name + ".log", "w")
                            log_file.write(str(current_line))
                            log_file.write("\n")
                            log_file.write(str(e.message))
                            log_file.write("\n")
                            continue
                        except StopIteration:
                            print (
                                "=== Finished inserting %d Documents to %s in db %s ===" % (
                                    idx, collection_name, dataset))
                            break
finally:
    server.stop()

