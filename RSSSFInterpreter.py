import re

from entities.Match import MatchTable, Match
from entities.Teams import Table


def interpret(file):
    with open(file, 'r', encoding='utf-8') as f:
        source = ""
        table = None
        matches = None
        for count, line in enumerate(f):
            if count == 0:
                source = line.strip()
                matches = MatchTable(source)
            # don't create new table after one is created
            # omit lines which don't contain 'Final Table' header
            if not table and line.__contains__('Final Table'):
                points_per_win = int(input('How many points per win were awarded?'))
                table = Table(source, points_per_win)
                next_line = next(f, '')
                # first strip all empty lines
                while not next_line.strip():
                    next_line = next(f, '')
                # then add rows to table until empty line encountered
                while next_line.strip():
                    # get position in table
                    split = next_line.find('.')
                    # read row only if line contains a dot
                    if split >= 0:
                        position = int(next_line[:split].strip())
                        next_line = next_line[split + 1:]
                        # TODO replace with length suggestion during first run
                        split = re.search(r'\s{2,}', next_line)
                        team = next_line[:split.start()]
                        next_line = next_line[split.end():]
                        # TODO extract goals first, then you can split the rest
                        line_data = next_line.split()
                        goals = line_data[4].split("-")
                        table.add_row(position, team, line_data[1], line_data[2], line_data[3], goals[0], goals[1])
                        if line_data.__contains__('Champions'):
                            table.standings.get(position).set_champions()
                        if line_data.__contains__('Relegated'):
                            table.standings.get(position).set_relegation()
                        if line_data.__contains__('Promoted'):
                            table.standings.get(position).set_promotion()
                    next_line = next(f, '')
                # TODO maybe create menu with numbers to choose which to use?
                table.add_competitions()
                table.add_relegations()
                table.add_promotions()
                # TODO add point deductions
                continue
            # so now we iterated over whole table
            # now let's break on encountering final table
            if line.__contains__('Final Table'):
                break
            # match regex
            score_re = re.search(r'[0-9\s]+-[0-9\s]+', line)
            if score_re:
                home = line[:score_re.start()].strip()
                away = line[score_re.end():].strip()
                # remove trailing notes
                note_re = re.search(r'\[.*\]', away)
                if note_re:
                    away = away[:note_re.start()].strip()
                score = score_re.group(0).split("-")
                home_score = score[0].strip()
                away_score = score[1].strip()
                matches.add_match(Match(home, away, home_score, away_score))
        return table, matches
