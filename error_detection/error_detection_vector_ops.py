import numpy as np
from fuzzywuzzy import fuzz
from sklearn.ensemble import IsolationForest as isolate


def duplicates(vector, data_type, fuzzy=False, fuzz_ratio_threshold=70):
    error = np.zeros_like(vector)

    if data_type.data_type != data_type.STRING or not data_type.is_consistent:
        return error

    for i, x in enumerate(vector):
        for y in vector[i + 1:]:
            error[i] = fuzz.ratio(x, y) > fuzz_ratio_threshold if fuzzy else x == y

    return error


def wrong_types(vector, data_type):
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


def outliers(vector, data_type):
    error = np.zeros_like(vector)

    if data_type.data_type != data_type.NUMBER or not data_type.is_consistent:
        return error

    vector = vector.reshape(-1, 1)
    forest = isolate()

    forest.fit(vector)
    forest_outliers = forest.predict(vector)
    error = np.asarray(forest_outliers == -1)

    return error
