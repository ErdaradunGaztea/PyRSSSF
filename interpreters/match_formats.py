import re

from entities.match import Match


def match_match_format_1(line):
    return re.match(
        r'[\w\s]+\s+[0-9]+-[0-9]+\s+[\w\s]+',
        line)


def match_match_format_2(line):
    return re.match(
        r'[^-]+\s+[\w\s]+\s+-\s+[\w\s]+\s+[0-9]+-[0-9]+',
        line)


def match_match_format_3(line):
    return re.match(
        r'[\w\s]+\s+-\s+[\w\s]+\s+[0-9]+:[0-9]+\s+\([0-9]+:[0-9]+\)',
        line)


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


def detect_match_format(line):
    if line is not None:
        if match_match_format_3(line):
            print("Detected match format no. 3.")
            return read_match_format_3
        if match_match_format_2(line):
            print("Detected match format no. 2.")
            return read_match_format_2
        if match_match_format_1(line):
            print("Detected match format no. 1.")
            return read_match_format_1
    return None
