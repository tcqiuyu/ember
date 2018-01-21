import csv

percentile = [0, 3, 5, 10, 25, 50, 75, 85, 90, 95, 97, 100]
bmi_col_idx = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58, 63, 68, 73]

import math


def get_cdc_bmi_chart_data():
    cdc_predict_bmi_percentile = {}
    with open("../data/growth_chart/bmi_percentile.csv", "rb") as f:
        rowdata = csv.reader(f)
        rownum = 0
        for row in rowdata:
            if rownum != 0:
                sex_and_age = row[0] + "," + str(int(math.ceil(float(row[1]))))
                bmi = []
                i = 0
                for col in row[2:]:
                    bmi.append(col)
                    i = i + 1
                cdc_predict_bmi_percentile[sex_and_age] = bmi
            rownum = rownum + 1
    # print cdc_predict_bmi_percentile
    return cdc_predict_bmi_percentile


def abbr_year_to_full_year(str):
    if int(str) > 80:
        return 1900 + int(str)
    else:
        return 2000 + int(str)


def get_nlsy97_data():
    with open("../rawData/NLSY97/NLSY97_Public/NLSY97_BMI.csv", "rb") as f:
        rawdata = csv.reader(f)
        col_name = rawdata.next()
        bmi_col_name = [col_name[i] for i in bmi_col_idx]
        candidates_data = []
        for row in rawdata:
            sex = row[1]
            bmi_data = [row[i] for i in bmi_col_idx]
            candidate = []
            for idx, bmi in enumerate(bmi_data):
                age = (abbr_year_to_full_year(bmi_col_name[idx].split("_")[1]) - int(row[2])) * 12
                if age <= 240:  # 53997 data points
                    sex_and_age = sex + "," + str(age)
                    candidate.append([sex_and_age, bmi])
            candidates_data.append(candidate)
    return candidates_data


def predict_percentile_range(candidates_data, cdc_data):
    y_predict = []
    y_actual = []

    for candidate in candidates_data:
        # print candidate
        for idx, yearly_data in enumerate(candidate):
            # print yearly_data
            if (yearly_data[1] != ''):
                sex_and_age = yearly_data[0]
                bmi = float(yearly_data[1])
                growth_chart_data = cdc_data.get(sex_and_age)
                # print sex_and_age
                # print growth_chart_data
                # print bmi
                for i in range(len(growth_chart_data) - 1):
                    bmi_a = float(growth_chart_data[i])
                    bmi_b = float(growth_chart_data[i + 1])
                    if bmi > bmi_a and bmi < bmi_b:
                        p_a = percentile[i]
                        p_b = percentile[i + 1]
                        p_calculated = p_a + (p_b - p_a) * (bmi - bmi_a) / (bmi_b - bmi_a)

                        # print p_a
                        # print p_calculated
    return y_predict, y_actual


if __name__ == '__main__':
    nlsy97_data = get_nlsy97_data()
    cdc_data = get_cdc_bmi_chart_data()
    #
    y_predict, y_actual = predict_percentile_range(nlsy97_data, cdc_data)
    print y_predict
