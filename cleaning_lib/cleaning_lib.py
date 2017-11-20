# 1. outlier detection
# 2. fuzzy matching
# 3. pattern matching

import csv
import json
import numpy as np
from fuzzywuzzy import fuzz
from pick import pick
from sklearn.ensemble import IsolationForest as isolate
import re


def read_file(csv_file, json_file):
    jsonfile = open(json_file, 'wb')
    with open(csv_file, 'rU') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        header = next(file_reader)
        fieldnames = header
        file_reader = csv.DictReader(csvfile, fieldnames)
        for row in file_reader:
            json.dump(row, jsonfile)
            jsonfile.write('\n')
    jsonfile.close()
    print(fieldnames)


def write_file(csv_file, content):
    with open(csv_file, 'ab') as csvfile:
        file_writer = csv.writer(csvfile, delimeter=',')
        for row in file_writer:
            print(row)


def get_columns(input_file, fieldnames, output_file):
    inputfile = open(input_file, 'rb')
    outputfile = open(output_file, 'wb')
    temp_dict = {}
    for column in fieldnames:
        col = []
        for line in inputfile:
            jsonobject = json.loads(line)
            col.append(jsonobject[column])
        inputfile.seek(0)
        temp_dict[column] = col
    print(temp_dict)
    json.dump(temp_dict, outputfile)
    inputfile.close()
    outputfile.close()


def fuzzy_matching(col):
    matched = []
    for x in range(len(col)):
        for y in range(x + 1, len(col)):
            fuzzyRatio = fuzz.ratio(col[x], col[y])
            if fuzzyRatio > 70:
                matched.append([x, y])
                print(str(col[x]) + " and " + str(col[y]) + " are similar: " + str(fuzzyRatio))
            # print "are these two the same?"
            else:
                print(str(col[x]) + " and " + str(col[y]) + " are different: " + str(fuzzyRatio))
                continue
    print("these are the indices of the similar strings: " + str(matched))
    return matched


def type_checking(col, colName):
    numberCount = 0
    letterCount = 0
    majority = ""
    colType = 0

    for x in range(0, len(col)):
        try:
            col[x] = float(col[x])
            numberCount += 1
        except ValueError:
            col[x] = str(col[x])
            letterCount += 1

    print("numberCount = " + str(numberCount))
    print("letterCount = " + str(letterCount))

    if numberCount > letterCount:
        majority = "numbers"
    else:
        majority = "letters/strings"

    title = "We detected that this column, " + str(colName) + ", has mostly " + majority + ". We have found " + str(numberCount) + " numbers and " + str(
        letterCount) + " letters/strings. What type should this column be??"
    options = ["string", "number"]

    selected = pick(options, title)

    if selected[0] == "string":
        colType = type("str")
    elif selected[0] == "number":
        colType = type(0.2)

    print(colType)
    newCol = filter_correct_types(col, colType)

    return newCol, colType


def filter_correct_types(col, correctType):
    print([x for x in col if (type(x) == correctType)])
    return [x for x in col if (type(x) == correctType)]


# def outlier_detection(col, options):
# 	stds = options[0]
# 	col_mean = np.mean(col)
# 	col_std = np.std(col)
# 	print [x for x in col if (x > col_mean + stds * col_std or x < col_mean - stds * col_std)]
# 	return [x for x in col if (x < col_mean + stds * col_std and x > col_mean - stds * col_std)]

def outlier_detection(col, options):
    # isolation forest to detect outliers, options to be added
    arr = np.asarray(col)
    arr = arr.reshape(-1, 1)
    forest = isolate()
    forest.fit(arr)
    forest_outliers = forest.predict(arr)
    outlier_index = []
    for i in range(len(forest_outliers)):
        if forest_outliers[i] == -1: outlier_index.append(i)
    for i in outlier_index:
        print("is " + str(col[i]) + " an outlier?")
    print("outliers detected in line numbers: " + str(outlier_index))
    return outlier_index


def detect_dup(col):
    # lets users choose what pk is by specifying col.
    dups = []
    for i in range(len(col)):
        for j in range(i + 1, len(col)):
            if col[i] == col[j]:
                dups.append([i, j])
                print("Are line " + str(i) + " and line " + str(j) + " duplicates?")


# def detect_irrelevant(col, restriction):
# 	# let users add restrictions to a certain col and remove lines from further processing
# 	# restriction parsed lambda function
# 	f = restriction
# 	irr = []
# 	for i in range(len(col)):
# 		if not (lambda f, i): irr.append(i)
# 	return irr

def lower_all(col):
    # standardize cases for further up detection/ row combine
    return [item.lower for item in col]


def strip_clean(col):
    # strip clean, for example ice_cream and ice cream is the same thing
    return [" ".join(re.split('\s|; |, |\*|\n|_|-', item)) for item in col]


def missing_non_numeric(col):
    # marks in missing non numerical values as missing, flags missing values
    missing = []
    for i in range(len(col)):
        if col[i] == "":
            col[i] = "missing"
            missing.append[i]  # TODO: BUG
    print(col)
    return missing


def missing_numeric(col, options):
    # flags missing numeric data and fill with 0
    # filling with mean?
    missing = []
    for i in range(len(col)):
        if col[i] == '':
            col[i] = 0
            missing.append[i]  # TODO: BUG
    print(col)
    return missing


def process_all_cols(input_file, f, output_file):
    # apply selected functions to all columns in file
    inputfile = open(input_file, 'rb')
    outputfile = open(output_file, 'wb')
    for line in inputfile:
        jsonobject = json.loads(line)
        temp_col = []
        temp_col = f(jsonobject.values()[0])
        print(temp_col)
        json.dump({jsonobject.keys()[0]: temp_col}, outputfile)
    inputfile.close()
    outputfile.close()


def open_file(filepath):
    with open(filepath) as columns:
        listOfCols = json.load(columns)
        # set column type flag, if type is 1 then it's numbers, if type is 2 then it's letters:
        for x in listOfCols:
            column_type = 0
            currentCol = listOfCols[x]
            typeChecked = type_checking(currentCol, x)
            z = typeChecked[0]
            column_type = typeChecked[1]

            if column_type == type("str"):
                title = "Would you like to check for potential misspelled entries?"
                options = ["yes", "no"]
                selected = pick(options, title)
                print(selected)
                if selected[0] == "yes":
                    y = fuzzy_matching(z)
                    print(y)

                title = "Would you like to check for any non-standard characters?"
                options = ["yes", "no"]
                selected = pick(options, title)
                if selected[0] == "yes":
                    y = strip_clean(z)
                    print("strip_clean " + str(y))
                else:
                    continue
            elif column_type == type(0.2):
                xo = outlier_detection(z, [1])
                print("outliers detected " + str(xo))


open_file('columns.json')

# read_file('/Users/Allison/Desktop/cleaning_lib/fruits.csv', '/Users/Allison/Desktop/cleaning_lib/test1.json')
# get_columns('/Users/Allison/Desktop/cleaning_lib/test1.json', ['fruits', 'In_stock', 'quantity'], '/Users/Allison/Desktop/cleaning_lib/columns1.json')

# ["distance from earth's center", 'depth', 'p-wave velocity', 's-wave velocity', 'density']
