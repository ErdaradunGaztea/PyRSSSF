import re

from entities.teams import TeamDictionary
from entities.topscorers import Topscorer


def match_topscorer_format_1(line):
    return re.match(
        r'\s*[0-9]+\s*-[\w\s()]+\[[\w\s]+\]',
        line)


def match_topscorer_format_2(line):
    return re.match(
        r'\s*[0-9]+\s*-?[\w\s]+\([\w\s]+\)',
        line)


def read_topscorer_format_1(line, current_goals, default_country):
    # update goal score, if present
    goalscore_re = re.match(r'\s*([0-9]+)\s*-\s*', line)
    if goalscore_re:
        current_goals = goalscore_re.group(1).strip()

    # read player team
    team_re = re.search(r'\s+\[([\w\s]+)\]', line)
    if not team_re:
        return None, current_goals
    team = TeamDictionary.get(team_re.group(1).strip())

    # extract player name (and nationality, if present)
    player_line = line[goalscore_re.end():team_re.start()] if goalscore_re else line[:team_re.start()]
    # TODO: insert if code of length 3, else ask and save answer
    nationality_re = re.search(r'\s+\((\w{3})\)', player_line)
    nationality = nationality_re.group(1).upper() if nationality_re else default_country
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
    team = TeamDictionary.get(team_re.group(1).strip())

    # extract player name (and nationality, if present)
    player_line = line[goalscore_re.end():team_re.start()] if goalscore_re else line[:team_re.start()]
    # TODO: is there any way of scraping nationality?
    return Topscorer(player_line.strip(), int(current_goals), team, default_country), current_goals


def detect_topscorer_format(line):
    if line is not None:
        if match_topscorer_format_2(line):
            print("Detected scorer format no. 2.")
            return read_topscorer_format_2
        elif match_topscorer_format_1(line):
            print("Detected scorer format no. 1.")
            return read_topscorer_format_1
    return None
