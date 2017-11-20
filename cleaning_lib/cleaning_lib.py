import re

import numpy as np
from fuzzywuzzy import fuzz
from sklearn.ensemble import IsolationForest as isolate


# Per-column cleaning operations


def fuzzy_match_column(col):
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


def check_type_column(column):
    # we need to check to see if the column types match up, but everything comes in as unicode
    # we try to convert each element in the column to a float. strings cannot be converted to floats, so we will convert it to a string instead.
    numberCount = 0
    letterCount = 0
    numberRows = []
    letterRows = []

    for x in range(0, len(column)):
        try:
            column[x] = float(column[x])
            numberRows.append(x)
            numberCount += 1
        except ValueError:
            column[x] = str(column[x])
            letterRows.append(x)
            letterCount += 1

        if letterCount >= numberCount:
            return column, numberRows
        else:
            return column, letterRows
            # this function returns the cleaned column array
            # it also returns the line numbers of the type we don't think it is (the lines where error might be)


def outlier_detection_column(col):
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


def detect_duplicates_column(col):
    # lets users choose what pk is by specifying col.
    dups = []
    for i in range(len(col)):
        for j in range(i + 1, len(col)):
            if col[i] == col[j]:
                dups.append([i, j])
                print("Are line " + str(i) + " and line " + str(j) + " duplicates?")


# Utilities

def lower_all(col):
    # standardize cases for further up detection/ row combine
    return [item.lower for item in col]


def strip_clean(col):
    # strip clean, for example ice_cream and ice cream is the same thing
    return [" ".join(re.split('\s|; |, |\*|\n|_|-', item)) for item in col]
