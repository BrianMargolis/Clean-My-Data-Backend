from cleaning_lib import cleaning_lib

class Cleaner():
    file_path = ""
    options = {}

    def __init__(self, file_path, options):
        self.file_path = file_path  # fully qualified path to the csv file on disk
        self.options = options  # object with necessary parameters for e

    def clean(self):
        if self.options["Fuzzy Matching"]:
            self.fuzzy_matching()

        if self.options["Outlier Detection"]:
            self.outlier_detection()

        # etc.
        pass

    # Should overwrite the file, return nothing
    def fuzzy_matching(self):
        pass

    # Should overwrite the file, return nothing
    def outlier_detection(self):
        pass
