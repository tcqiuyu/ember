import csv
import os
import re

import xlrd

# Data Folder Path
data_root = "../rawData/"
addHealth_dicts_path = data_root + "Add Health/"


def has_variable(row):
    # iterate current row
    for cell in row:
        # rules that row has variable cell
        if isinstance(cell.value, basestring) and cell.value.isupper() and len(
                cell.value) > 2 and not cell.value.__contains__(" "):
            return str(cell.value)
    return -1


def extract_wave_1_to_3():
    with open('output/question_text/add_health_question.tsv', 'wb') as output_file:
        output_writer = csv.writer(output_file, delimiter="\t")
        # iterate over codebooks
        for subdir, dir, files in os.walk(addHealth_dicts_path):
            for file in files:
                # W4 has different format
                if file.find("codebook") != -1 and file.endswith("xlsx") and file.startswith(
                        "~") is False and file.find("W4") == -1:
                    file_path = os.path.join(subdir, file)
                    wb = xlrd.open_workbook(file_path)

                    for sh in wb.sheets():

                        pre_question = ""

                        for rowx in range(sh.nrows):
                            # Question text at col 0
                            question = unicode(sh.cell_value(rowx, 0))
                            variable = has_variable(sh.row(rowx))

                            # in case there are multiple lines, such as
                            # "12.   In what country were you born?
                            # [computer supplied look-up table]"
                            question_split = question.split('\n')

                            for line in question_split:
                                # find text starts with "1. 2. ... etc."
                                # if the row does not have variable cell, it has subquestions
                                if re.match("\d+\.\s.*", line) and variable == -1:
                                    pre_question = line
                                    print line
                                elif re.match("\d+\.\s.*", line) and variable != -1:
                                    pre_question = ""
                                    question = line.replace(u'\u2018', "'").replace(u'\u2019',"'")
                                    # question = question.split("  ")[-1]
                                    # question = re.compile("\d+\.\s.*").split(question)[0]
                                    question = re.split("\d+\.\s+",question)[-1]
                                    output = [variable, question.encode('utf-8')]
                                    print output
                                    output_writer.writerow(output)
                                    break
                                elif len(question_split) == 1 and variable != -1:
                                    question = (pre_question + " " + line).replace(u'\u2018', "'").replace(u'\u2019',"'")
                                    # question = question.split("  ")[-1]
                                    # question = re.compile("\d+\.\s.*").split(question)[0]
                                    question = re.split("\d+\.\s+", question)[-1]
                                    output = [variable, question.encode('utf-8')]
                                    print output
                                    output_writer.writerow(output)
                                    break


def extract_wave_4():
    with open('output/question_text/add_health_question.tsv', 'ab') as output_file:
        output_writer = csv.writer(output_file, delimiter="\t")
        # iterate over codebooks
        for subdir, dir, files in os.walk(addHealth_dicts_path):
            for file in files:
                # W4 has different format
                if file.find("codebook") != -1 and file.endswith("xlsx") and file.startswith(
                        "~") is False and file.find("W4") != -1:
                    file_path = os.path.join(subdir, file)
                    wb = xlrd.open_workbook(file_path)
                    for sh in wb.sheets():
                        for rowx in range(sh.nrows):
                            variable = ""
                            first_cell = sh.cell_value(rowx, 0)
                            if isinstance(first_cell, basestring) and first_cell.isupper() and len(
                                    first_cell) > 2 and not first_cell.__contains__(" "):
                                variable = first_cell
                                idx = 0
                                for cell in reversed(sh.row(rowx)):
                                    idx = idx + 1
                                    if isinstance(cell.value, unicode) and cell.value != "" and idx != len(
                                            sh.row(rowx)):
                                        question = unicode(cell.value)
                                        question = question.split("\n")[0]
                                        question = re.split("\d+[A-Z]?\.\s+", question)[-1]
                                        print variable + ":" + question
                                        output = [variable, question.encode('utf-8')]
                                        output_writer.writerow(output)
                                        break


if __name__ == '__main__':
    extract_wave_1_to_3()
    extract_wave_4()
