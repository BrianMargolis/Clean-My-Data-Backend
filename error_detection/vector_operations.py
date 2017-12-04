import numpy as np
from fuzzywuzzy import fuzz
from sklearn.ensemble import IsolationForest as isolate


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
