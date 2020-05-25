class HeaderDetector:
    expecting_header = False
    possible_header = False
    header = False

    @staticmethod
    def detect(line):
        if not HeaderDetector.expecting_header:
            if not line.strip():
                HeaderDetector.expecting_header = True
        elif not HeaderDetector.possible_header:
            if line.strip():
                HeaderDetector.possible_header = True
        elif not HeaderDetector.header:
            if not line.strip():
                HeaderDetector.header = True
            else:
                HeaderDetector.expecting_header = False
                HeaderDetector.possible_header = False

    @staticmethod
    def clear():
        HeaderDetector.expecting_header = False
        HeaderDetector.possible_header = False
        HeaderDetector.header = False
