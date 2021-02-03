import re

from interpreters.header_detector import HeaderDetector
from entities.Match import MatchTable, Match


def detect_match_format(line):
    if re.match(r'[\w\s]+\s+-\s+[\w\s]+\s+[0-9]+:[0-9]+\s+\([0-9]+:[0-9]+\)', line):
        print("Detected match format no. 3.")
        return 3
    elif re.match(r'[^-]+\s+[\w\s]+\s+-\s+[\w\s]+\s+[0-9]+-[0-9]+', line):
        print("Detected match format no. 2.")
        return 2
    elif re.match(r'[\w\s]+\s+[0-9]+-[0-9]+\s+[\w\s]+', line):
        print("Detected match format no. 1.")
        return 1
    return None


def read_match_format_1(line, notes, match_length, note_prompt):
    # match regex
    awd_re = re.search(r'\sawd\s', line)
    if awd_re:
        # TODO: handle forfeits
        return None, match_length

    score_re = re.search(r'[0-9\s]+-[0-9\s]+', line)
    if not score_re:
        return None, match_length

    if not match_length:
        split = re.search(r'\[', line)
        match_length = split.start() if split else len(line)
        match_length_input = input("Predicted length of spaces for a match is {0}. Leave empty if "
                                   "agree, else input correct match result length.".format(match_length))
        if match_length_input:
            match_length = int(match_length_input)

    match_line = line[:match_length]
    home = match_line[:score_re.start()].strip()
    away = match_line[score_re.end():].strip()
    score = score_re.group(0).split("-")
    home_score = score[0].strip()
    away_score = score[1].strip()
    match = Match(home, away, home_score, away_score)

    # continue only if line is not skipped (None condition below is equivalent to this)
    if match.home is None or match.away is None:
        return None, match_length

    # if a note detected
    if line[match_length:].__contains__('['):
        note_input = input(note_prompt.format(home, home_score, away_score, away))
        previous_note_match = re.match(r'[0-9]+$', note_input)
        if previous_note_match:
            match.add_note((previous_note_match.group(), notes.get(previous_note_match)))
        elif note_input:
            key = len(notes) + 2
            notes.__setitem__(key, note_input)
            match.add_note((key, note_input))
            print("New note added:\n{0}: {1}".format(key, note_input))
    return match, match_length


def read_match_format_2(line, notes, match_length, note_prompt):
    score_re = re.search(r'[0-9]+\s*-\s*[0-9]+', line)
    if not score_re:
        return None, match_length

    if not match_length:
        date_re = re.search(r'[0-9]+\.\w{3}\.[0-9]{2}', line)
        if not date_re:
            print("Invalid format detected!\nLine: {0}".format(line))
            return None, match_length
        match_length = (date_re.end(), score_re.end())

    match_line = line[match_length[0]:match_length[1]]
    first_hyphen = re.search(r'\s-\s', match_line)
    home = match_line[:first_hyphen.start()].strip()
    away = match_line[first_hyphen.end():(score_re.start() - match_length[0])].strip()
    score = score_re.group(0).split("-")
    home_score = score[0].strip()
    away_score = score[1].strip()
    match = Match(home, away, home_score, away_score)

    # continue only if line is not skipped (None condition below is equivalent to this)
    if match.home is None or match.away is None:
        return None, match_length

    # if a note detected
    if line[match_length[1]:].__contains__('['):
        note_input = input(note_prompt.format(home, home_score, away_score, away))
        previous_note_match = re.match(r'[0-9]+$', note_input)
        if previous_note_match:
            match.add_note((previous_note_match.group(), notes.get(previous_note_match)))
        elif note_input:
            key = len(notes) + 2
            notes.__setitem__(key, note_input)
            match.add_note((key, note_input))
            print("New note added:\n{0}: {1}".format(key, note_input))
    return match, match_length


def read_match_format_3(line, notes, match_length, note_prompt):
    score_re = re.search(r'([0-9]+:[0-9]+)\s+\([0-9]+:[0-9]+\)', line)
    if not score_re:
        return None, match_length

    if not match_length:
        split = re.search(r'\[', line)
        match_length = split.start() if split else len(line)
        match_length_input = input("Predicted length of spaces for a match is {0}. Leave empty if "
                                   "agree, else input correct match result length.".format(match_length))
        if match_length_input:
            match_length = int(match_length_input)

    first_hyphen = re.search(r'\s-\s', line)
    home = line[:first_hyphen.start()].strip()
    away = line[first_hyphen.end():score_re.start()].strip()
    score = score_re.group(1).split(":")
    home_score = score[0].strip()
    away_score = score[1].strip()
    match = Match(home, away, home_score, away_score)

    # continue only if line is not skipped (None condition below is equivalent to this)
    if match.home is None or match.away is None:
        return None, match_length

    return match, match_length


def read_matches(f, source):
    # create match matrix
    print("### Creating match matrix...")
    matches = MatchTable(source)
    # declare match length variable to apply condition to later
    match_length = None

    note_prompt = "Note detected for a match: {0} {1}:{2} {3}.\n" \
                  "Input text to append a note to this match.\n" \
                  "Input single number to link this match with previous note.\n" \
                  "Leave empty if no note necessary."
    notes = dict()

    # first detect match format
    next_line = next(f, None)
    match_format = detect_match_format(next_line)
    while not match_format:
        next_line = next(f, None)
        match_format = detect_match_format(next_line)

    stop = False
    line = ""
    while not stop and next_line is not None:
        while not HeaderDetector.header:
            line = next_line

            match = None
            if match_format == 1:
                match, match_length = read_match_format_1(line, notes, match_length, note_prompt)
            elif match_format == 2:
                match, match_length = read_match_format_2(line, notes, match_length, note_prompt)
            elif match_format == 3:
                match, match_length = read_match_format_3(line, notes, match_length, note_prompt)

            if match:
                matches.add_match(match)
                # if match detected, it's definitely not a header
                HeaderDetector.clear()

            next_line = next(f, None)
            if next_line is None:
                return matches
            HeaderDetector.detect(next_line)
        stop = input('Header detected: "{0}". Type "y" to continue scraping. '
                     'Leave empty otherwise.'.format(line)) != 'y'

        next_line = next(f, None)
        if next_line is None:
            return matches
        HeaderDetector.detect(next_line)
    return matches, line
