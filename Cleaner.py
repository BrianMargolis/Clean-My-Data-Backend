import numpy as np

from error_detection import error_detection


class Cleaner():
    file_name = ""
    options = {}

    data = None
    errors = None

    def __init__(self, file_name, options):
        self.file_name = file_name
        self.options = options

        self.data = np.genfromtxt(file_name, delimiter=',')
        if options['file_has_headers']:
            self.data = self.data[1:]

        self.errors = np.zeros_like(self.data)

    def identify_errors(self):
        error_counts = np.zeros_like(self.data)
        if "Duplicates" in self.options:
            error_counts += self.duplicates()

        if "Outliers" in self.options:
            error_counts += self.outliers()

        if "Wrong Types" in self.options:
            error_counts += self.wrong_types()

        self.errors = error_counts > 0

    def duplicates(self):
        return error_detection.duplicates(self.data)

    def outliers(self):
        return error_detection.outliers(self.data)

    def wrong_types(self):
        return error_detection.wrong_types(self.data)

    def get_errors(self):
        return self.errors

    def get_column_error_rates(self):
        assert self.errors is not None
        return error_detection.get_column_error_rates(self.errors)

    def get_column_statistics(self):
        assert self.data is not None

        if "alpha" in self.options:
            return error_detection.get_column_statistics(self.data, self.options['alpha'])
        else:
            return error_detection.get_column_statistics(self.data)
