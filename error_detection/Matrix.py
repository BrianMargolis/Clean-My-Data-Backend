import numpy as np


class Matrix:
    data = None
    types = None

    def __init__(self, data):
        self.data = data
        self.types = []

        for column in data.T:
            self.types.append(self.get_type(column))

    @staticmethod
    def get_type(vector):
        numbers = 0
        strings = 0

        for i, item in enumerate(vector):
            try:
                float(item)
                numbers += 1
            except ValueError:
                strings += 1

        t = Type.NUMBER if numbers > strings else Type.STRING
        is_consistent = min(numbers, strings) == 0
        return Type(t, is_consistent)


class Type:
    NUMBER, STRING = range(2)

    data_type = None
    is_consistent = None

    def __init__(self, data_type, is_consistent):
        self.data_type = data_type
        self.is_consistent = is_consistent
