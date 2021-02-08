from entities.match import MatchTable
from interpreters.header_detector import HeaderDetector
from interpreters.match_formats import detect_match_format

note_prompt = "Note detected for a match: {0} {1}:{2} {3}.\n" \
              "Input text to append a note to this match.\n" \
              "Input single number to link this match with previous note.\n" \
              "Leave empty if no note necessary."


class MatchInterpreter:
    def __init__(self):
        self.matches = None
        # declare match length variable to apply condition to later
        self.match_length = None
        self.notes = dict()

    def __read_matches(self, f, source):
        # create match matrix
        print("### Creating match matrix...")
        self.matches = MatchTable(source)

        # first detect match format
        line = next(f, None)
        match_format_func = detect_match_format(line)
        while not match_format_func:
            line = next(f, None)
            match_format_func = detect_match_format(line)

        stop = False
        while not stop and line is not None:
            while not HeaderDetector.header:
                match, self.match_length = match_format_func(line, self.notes, self.match_length, note_prompt)

                if match:
                    self.matches.add_match(match)
                    # if match detected, it's definitely not a header
                    HeaderDetector.clear()

                line = next(f, None)
                if line is None:
                    return line
                HeaderDetector.detect(line)
            stop = input('Header detected: "{0}". Type "y" to continue scraping. '
                         'Leave empty otherwise.'.format(line)) != 'y'

            line = next(f, None)
            HeaderDetector.detect(line)

        return line

    def run(self, f, source):
        line = self.__read_matches(f, source)
        return self.matches, line
