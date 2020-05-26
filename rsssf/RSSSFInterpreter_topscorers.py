import re

from entities.Teams import team_dictionary
from entities.Topscorers import TopscorerTable, Topscorer


def detect_topscorer_format(line):
    if re.match(r'\s*[0-9]+\s*-?[\w\s]+\([\w\s]+\)', line):
        print("Detected scorer format no. 2.")
        return 2
    elif re.match(r'\s*[0-9]+\s*-[\w\s\(\)]+\[[\w\s]+\]', line):
        print("Detected scorer format no. 1.")
        return 1
    return None


def read_topscorer_format_1(line, current_goals, default_country):
    # update goal score, if present
    goalscore_re = re.match(r'\s*([0-9]+)\s*-\s*', line)
    if goalscore_re:
        current_goals = goalscore_re.group(1).strip()

    # read player team
    team_re = re.search(r'\s+\[([\w\s]+)\]', line)
    if not team_re:
        return None, current_goals
    team = team_dictionary.get(team_re.group(1).strip())

    # extract player name (and nationality, if present)
    player_line = line[goalscore_re.end():team_re.start()] if goalscore_re else line[:team_re.start()]
    # TODO: insert if code of length 3, else ask and save answer
    nationality_re = re.search(r'\s+\((\w{3})\)', player_line)
    nationality = default_country
    if nationality_re:
        nationality = nationality_re.group(1).upper()
    name = player_line[:nationality_re.start()].strip() if nationality_re else player_line.strip()
    return Topscorer(name, int(current_goals), team, nationality), current_goals


def read_topscorer_format_2(line, current_goals, default_country):
    # update goal score, if present
    goalscore_re = re.match(r'\s*([0-9]+)\s+-?\s*', line)
    if goalscore_re:
        current_goals = goalscore_re.group(1).strip()

    # read player team
    team_re = re.search(r'\s+\(([\w\s]+)\)', line)
    if not team_re:
        return None, current_goals
    team = team_dictionary.get(team_re.group(1).strip())

    # extract player name (and nationality, if present)
    player_line = line[goalscore_re.end():team_re.start()] if goalscore_re else line[:team_re.start()]
    # TODO: is there any way of scraping nationality?
    return Topscorer(player_line.strip(), int(current_goals), team, default_country), current_goals


def read_topscorers(f, line):
    # look for topscorers header
    while line is not None and not re.search(r'top\s?scorers', line.lower()):
        line = next(f, None)

    # first detect topscorer format
    line = next(f, None)
    topscorer_format = detect_topscorer_format(line)
    while line is not None and not topscorer_format:
        line = next(f, None)
        topscorer_format = detect_topscorer_format(line)

    if line is None:
        return None

    print("### Creating topscorers table...")
    table = TopscorerTable()

    # extract topscorers
    current_goals = 0
    default_country = input("What is the 3-letter code of the default nationality of topscorers?")
    while line is not None and line.strip():
        player = None
        if topscorer_format == 1:
            player, current_goals = read_topscorer_format_1(line, current_goals, default_country)
        elif topscorer_format == 2:
            player, current_goals = read_topscorer_format_2(line, current_goals, default_country)

        if player:
            table.add_topscorer(player)
        line = next(f, None)
    return table
