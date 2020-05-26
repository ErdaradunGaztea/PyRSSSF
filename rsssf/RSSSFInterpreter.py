import re

from entities.Teams import Table
from rsssf.RSSSFInterpreter_matches import read_matches
from rsssf.RSSSFInterpreter_topscorers import read_topscorers


# TODO: predict h1 headers by this condition:
#  if a non-empty line is preceded and succeeded by at least one empty line, then it might be a h1 header
# TODO: predict match description type: either TeamA 0-0 TeamB or TeamA - TeamB 0-0


def read_table(f, source):
    # create standings table
    print("### Creating table...")
    points_per_win = int(input('How many points per win were awarded?'))
    table = Table(source, points_per_win)
    # declare team name length variable to apply condition to later
    team_name_length = None

    # first strip all empty lines
    line = next(f, None)
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
    return table


def update_table(table):
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


def interpret(file):
    table_header = "final table".lower()
    with open(file, 'r', encoding='utf-8') as f:
        # read first line with source
        source = next(f, None).strip()

        # find table header
        line = next(f, None)
        while line is not None and not line.lower().__contains__(table_header):
            line = next(f, None)

        table = read_table(f, source)
        update_table(table)
        matches, line = read_matches(f, source)
        topscorers = read_topscorers(f, line)

    return table, matches, topscorers
