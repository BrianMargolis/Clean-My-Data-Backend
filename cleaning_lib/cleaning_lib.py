import re

import numpy as np
from fuzzywuzzy import fuzz
from sklearn.ensemble import IsolationForest as isolate


def extend_vector_op_to_matrix(input_matrix, vector_op, vector_op_args=[]):
    output_matrix = []

    # Is transposing a huge matrix expensive?
    # https://stackoverflow.com/questions/19479384/is-numpy-transpose-reordering-data-in-memory/19479436#19479436
    # TLDR: no, it just changes the stride of the array.
    for columns in input_matrix.T:
        output_matrix.append(vector_op(columns, *vector_op_args))

    return np.array(output_matrix).T


# Per-column cleaning operations


def duplicates(vector, fuzzy=False, fuzz_ratio_threshold=70):
    error = np.zeros_like(vector)

    for x in range(len(vector)):
        for y in range(x + 1, len(vector)):
            error[x] = fuzz.ratio(x, y) > fuzz_ratio_threshold if fuzzy else x == y

    return error


def wrong_types(vector):
    numbers = np.zeros_like(vector)
    strings = np.zeros_like(vector)

    for i, item in enumerate(vector):
        try:
            float(item)
            numbers[i] = True
        except ValueError:
            strings[i] = True

    is_numbers = numbers.sum() > strings.sum()
    return strings if is_numbers else numbers


def outliers(vector):
    vector = vector.reshape(-1, 1)

    forest = isolate()
    forest.fit(vector)
    forest_outliers = forest.predict(vector)
    error = [forest_outliers == 1]

    return error
