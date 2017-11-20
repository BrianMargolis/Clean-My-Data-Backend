from cleaning_lib import cleaning_lib

class Cleaner():
    file_path = ""
    options = {}

    def __init__(self, file_path, options):
        self.file_path = file_path  # fully qualified path to the csv file on disk
        self.options = options  # object with necessary parameters for e

    def identify_errors(self):
        pass
        errors = []
        if self.options["Fuzzy Matching"]:
            errors += self.fuzzy_matching()

        if self.options["Outlier Detection"]:
            errors += self.outlier_detection()

        # etc.
        return errors

    def clean_data(self, errors):
        pass

    # Should overwrite the file, return nothing
    def fuzzy_matching(self):
        pass

    # Should overwrite the file, return nothing
    def outlier_detection(self):
        pass
