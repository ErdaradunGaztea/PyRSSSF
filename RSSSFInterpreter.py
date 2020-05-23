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
            if not table and line.lower().__contains__('final table'):
                points_per_win = int(input('How many points per win were awarded?'))
                table = Table(source, points_per_win)
                next_line = next(f, '')
                # declare team name length variable to apply condition to later
                team_name_length = None
                # first strip all empty lines
                while not next_line.strip():
                    next_line = next(f, '')
                # then add rows to table until empty line encountered
                while next_line.strip():
                    # get position in table
                    split = next_line.find('.')
                    # read row only if line contains a dot (risky but working)
                    if split >= 0:
                        position = int(next_line[:split].strip())
                        next_line = next_line[split + 1:]
                        if not team_name_length:
                            split = re.search(r'\s{2,}', next_line)
                            team_name_length = input("Predicted length of spaces for team name is {0}. Leave empty if "
                                                     "agree, else input correct team name length.".format(split.end()))
                            team_name_length = int(team_name_length) if team_name_length else split.end()
                        team = next_line[:team_name_length].strip()
                        next_line = next_line[team_name_length:].strip()
                        # extract goal data
                        goal_data = re.search(r'[0-9]+\s*-\s*[0-9]+', next_line)
                        goals = goal_data.split("-")
                        # extract matches played, wins, draws and losses
                        match_data = next_line[:goal_data.start()].split()
                        table.add_row(position, team, match_data[1], match_data[2], match_data[3],
                                      goals[0].strip(), goals[1].strip())
                        # extract points and any additional notes
                        line_data = next_line[goal_data.end():].split()
                        if line_data.__contains__('Champions'):
                            table.standings.get(position).set_champions()
                        if line_data.__contains__('Relegated'):
                            table.standings.get(position).set_relegation()
                        if line_data.__contains__('Promoted'):
                            table.standings.get(position).set_promotion()
                    next_line = next(f, '')
                menu_prompt = """
                Table enchancements available:\n
                * press 1 to add promotions to higher league\n
                * press 2 to add relegations to lower league\n
                * press 3 to add qualifications to international competitions\n
                Leave empty to finalize.
                """
                menu_choice = input(menu_prompt)
                while menu_choice:
                    if menu_choice == '1':
                        table.add_promotions()
                    if menu_choice == '2':
                        table.add_relegations()
                    if menu_choice == '3':
                        table.add_competitions()
                    menu_choice = input(menu_prompt)
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
