import numpy as np

from error_detection import error_detection, post_processing
from error_detection.Matrix import Matrix


class ErrorDetector():
    file_name = ""
    options = {}

    data = None
    matrix = None
    errors = None

    def __init__(self, file_name, options):
        self.file_name = file_name
        self.options = options

        self.data = np.genfromtxt(file_name, dtype=object, delimiter=',')
        if options['file_has_headers']:
            self.data = self.data[1:]

        self.matrix = Matrix(self.data)

        self.errors = np.zeros_like(self.data)

    def identify_errors(self):
        error_counts = np.zeros_like(self.data)
        if self.options['duplicates']['enabled']:
            error_counts += self.duplicates()

        if self.options['outliers']['enabled']:
            error_counts += self.outliers()

        if self.options['wrong_types']['enabled']:
            error_counts += self.wrong_types()

        self.errors = error_counts > 0

    def duplicates(self):
        options = self.options['duplicates']['options']
        fuzzy, fuzzy_ratio_threshold = False, 70

        for option in options:
            if option['name'] == 'fuzzy':
                fuzzy = option['value']
            elif option['name'] == 'fuzzy_ratio_threshold':
                fuzzy_ratio_threshold = float(option['value'])

        return error_detection.duplicates(self.matrix, fuzzy, fuzzy_ratio_threshold)

    def outliers(self):
        return error_detection.outliers(self.matrix)

    def wrong_types(self):
        return error_detection.wrong_types(self.matrix)

    def get_errors(self):
        return self.errors

    def get_column_error_rates(self):
        assert self.errors is not None
        return post_processing.get_column_error_rates(self.errors)

    def get_column_summary_statistics(self):
        assert self.matrix is not None

        return post_processing.get_column_summary_statistics(self.matrix)
