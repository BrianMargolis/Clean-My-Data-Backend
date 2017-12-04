import numpy as np

from error_detection import error_detection


class Cleaner():
    file_name = ""
    options = {}

    data = None

    def __init__(self, file_name, options):
        self.file_name = file_name
        self.options = options

        self.data = np.genfromtxt(file_name, delimiter=',')
        self.errors = np.zeros_like(self.data)

    def identify_errors(self):
        error_counts = np.zeros_like(self.data)
        if "Fuzzy Matching Enabled" in self.options and self.options["Fuzzy Matching Enabled"]:
            error_counts += self.duplicates()

        if "Outlier Detection Enabled" in self.options and self.options["Outlier Detection Enabled"]:
            error_counts += self.outliers()

        if "Duplicate Detection Enabled" in self.options and self.options["Duplicate Detection Enabled"]:
            error_counts += self.wrong_types()

        self.errors = error_counts > 0

    def duplicates(self):
        return error_detection.duplicates(self.data)

    def outliers(self):
        return error_detection.outliers(self.data)

    def wrong_types(self):
        return error_detection.wrong_types(self.data)
