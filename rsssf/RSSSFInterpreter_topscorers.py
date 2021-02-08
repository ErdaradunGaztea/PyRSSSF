import re

from entities.teams import TeamDictionary
from entities.topscorers import TopscorerTable, Topscorer


def read_topscorers(f, line):
    # look for topscorers header
    while line is not None and not re.search(r'top\s?scorers', line.lower()):
        line = next(f, None)

    if line is None:
        return None

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
