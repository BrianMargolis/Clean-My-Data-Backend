import numpy as np

from error_detection import error_detection, post_processing
from error_detection.Matrix import Matrix


class ErrorDetector:
    file_name = ""
    options = {}  # Dictionary of options and parameters for error identification.

    data = None
    matrix = None
    errors = None

    def __init__(self, file_name, options):
        """
        Create an error detector object. Run identify_errors 
        
        :param file_name: fully qualified path to the CSV file
        :param options: options dictionary from the HTTP request
        """
        self.file_name = file_name
        self.options = options

        self.data = np.genfromtxt(file_name, dtype=object, delimiter=',')
        if options['file_has_headers']:
            self.data = self.data[1:]

        self.matrix = Matrix(self.data)

        self.errors = np.zeros_like(self.data)

    def identify_errors(self):
        """
        Runs the error detection functions specified in the options dictionary.
        """
        assert self.data is not None and self.matrix is not None

        error_counts = np.zeros_like(self.data)

        if self.options['duplicates']['enabled']:
            error_counts += self.duplicates()

        if self.options['outliers']['enabled']:
            error_counts += self.outliers()

        if self.options['wrong_types']['enabled']:
            error_counts += self.wrong_types()

        self.errors = error_counts > 0

    def duplicates(self):
        """
        Get a boolean matrix representing the locations of duplicates in the data set.
        """
        options = self.options['duplicates']['options']
        fuzzy, fuzzy_ratio_threshold = False, 70

        for option in options:
            if option['name'] == 'fuzzy':
                fuzzy = option['value']
            elif option['name'] == 'fuzzy_ratio_threshold':
                fuzzy_ratio_threshold = float(option['value'])

        return error_detection.duplicates(self.matrix, fuzzy, fuzzy_ratio_threshold)

    def outliers(self):
        """
        Get a boolean matrix representing the locations of outliers in the data set.
        """
        return error_detection.outliers(self.matrix)

    def wrong_types(self):
        """
        Get a boolean matrix representing the locations of data that has the wrong type.
        """
        return error_detection.wrong_types(self.matrix)

    def get_errors(self):
        return self.errors

    def get_column_error_rates(self):
        """
        Get an array of the error rates expressed as a decimal in string form.
        """
        assert self.errors is not None
        return post_processing.get_column_error_rates(self.errors)

    def get_column_summary_statistics(self):
        """
        Get a summary statistics object with information about the mean, standard deviation, confidence interval, and outliers of each column.
        """
        assert self.matrix is not None

        return post_processing.get_column_summary_statistics(self.matrix)
