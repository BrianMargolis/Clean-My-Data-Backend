class Cleaner():
    file_path = ""
    options = {}

    def __init__(self, file_path, options):
        self.file_path = file_path
        self.options = options

    def clean(self):
        if self.options["Fuzzy Matching"]:
            self.fuzzy_matching()

    def fuzzy_matching(self):
        pass

