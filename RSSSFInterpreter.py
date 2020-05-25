import re

from entities.Match import MatchTable, Match
from entities.Teams import Table


def get_next(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None


def interpret(file):
    table_header = "final table".lower()
    with open(file, 'r', encoding='utf-8') as f:
        # read first line with source
        source = get_next(f).strip()

        # find table header
        line = get_next(f)
        while line is not None and not line.lower().__contains__(table_header):
            line = get_next(f)

        # create standings table
        print("### Creating table...")
        points_per_win = int(input('How many points per win were awarded?'))
        table = Table(source, points_per_win)
        # declare team name length variable to apply condition to later
        team_name_length = None

        # first strip all empty lines
        line = get_next(f)
        while not line.strip():
            line = next(f, '')

        # then add rows to table until empty line encountered
        while line.strip():
            # get position in table
            split = line.find('.')
            # read row only if line contains a dot (risky but working)
            if split >= 0:
                position = int(line[:split].strip())
                line = line[split + 1:]
                if not team_name_length:
                    split = re.search(r'\s{2,}', line)
                    team_name_length = input("Predicted length of spaces for team name is {0}. Leave empty if "
                                             "agree, else input correct team name length.".format(split.end()))
                    team_name_length = int(team_name_length) if team_name_length else split.end()
                team = line[:team_name_length].strip()
                line = line[team_name_length:].strip()
                # extract goal data
                goal_data = re.search(r'[0-9]+\s*-\s*[0-9]+', line)
                goals = goal_data.group(0).split("-")
                # extract matches played, wins, draws and losses
                match_data = line[:goal_data.start()].split()
                table.add_row(position, team, match_data[1], match_data[2], match_data[3],
                              goals[0].strip(), goals[1].strip())
                # extract points and any additional notes
                line_data = line[goal_data.end():].split()
                if line_data.__contains__('Champions'):
                    table.standings.get(position).set_champions()
                if line_data.__contains__('Relegated'):
                    table.standings.get(position).set_relegation()
                if line_data.__contains__('Promoted'):
                    table.standings.get(position).set_promotion()
            line = next(f, '')

        # fill result table with additional info
        menu_prompt = "Table enchancements available:\n" \
                      "* press 1 to add promotions to higher league\n" \
                      "* press 2 to add relegations to lower league\n" \
                      "* press 3 to add qualifications to international competitions\n" \
                      "Leave empty to finalize table creation."
        menu_choice = input(menu_prompt)
        while menu_choice:
            if menu_choice == '1':
                table.add_promotions()
            if menu_choice == '2':
                table.add_relegations()
            if menu_choice == '3':
                table.add_competitions()
            menu_choice = input(menu_prompt)

        # create match matrix
        print("### Creating match matrix...")
        matches = MatchTable(source)
        # declare match length variable to apply condition to later
        match_length = None

        note_prompt = "Note detected for a match: {0} {1}-{2} {3}.\n" \
                      "Input text to append a note to this match.\n" \
                      "Input single number to link this match with previous note.\n" \
                      "Leave empty if no note necessary."
        notes = dict()

        # now continue until encountering final table
        while line is not None and not line.lower().__contains__(table_header):
            # match regex
            score_re = re.search(r'[0-9\s]+-[0-9\s]+', line)
            if score_re:
                if not match_length:
                    split = re.search(r'\[', line)
                    match_length = split.start() if split else len(line)
                    match_length_input = input("Predicted length of spaces for a match is {0}. Leave empty if "
                                               "agree, else input correct match result length.".format(match_length))
                    if match_length_input:
                        match_length = int(match_length_input)
                # TODO: allow to skip match line if suspicious about strange key
                match_line = line[:match_length]
                home = match_line[:score_re.start()].strip()
                away = match_line[score_re.end():].strip()
                score = score_re.group(0).split("-")
                home_score = score[0].strip()
                away_score = score[1].strip()
                match = Match(home, away, home_score, away_score)
                # continue only is line is not skipped (None condition below is equivalent to this)
                if match.home is not None and match.away is not None:
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
                    matches.add_match(match)
            line = get_next(f)

        # TODO: create top scorers
        print("### NOT creating top scorers table...")

    return table, matches
