import re


def set_champions_relegation_promotion(table, position, data):
    if data.__contains__('Champions'):
        table.standings.get(position).set_champions()
    if data.__contains__('Relegated'):
        table.standings.get(position).set_relegation()
    if data.__contains__('Promoted'):
        table.standings.get(position).set_promotion()
    return table


def match_table_format_1(line):
    """
    Relies on name not containing any numbers. Example line:
     2 Besiktas JK Istanbul     34  19  12   3  49  19  50 UEFA Cup
    """
    return re.match(
        r'\s*[0-9]+\s+[\D]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[\w\s]*',
        line)


# TODO: reimplement
def match_table_format_2(line):
    return None
    # return re.match(r'.+', line)


def read_table_format_1(f, line, table):
    while line.strip():
        # process the line only if it fits the regex
        if match_table_format_1(line):
            # get position in table
            position_re = re.search(r'\s*([0-9]+)', line)
            position = int(position_re.group(1))
            line = line[position_re.end():]
            # find matches, goals and points data
            data = re.search(
                r'([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([\w\s]*)',
                line)
            # extract team name and remove additional info in parentheses ()
            team = re.sub(r'\([^)]+\)', '', line[:data.start()]).strip()
            table.add_row(position, team, data.group(2), data.group(3), data.group(4),
                          data.group(5), data.group(6))
            # extract points and any additional notes
            table = set_champions_relegation_promotion(table, position, data.group(8).split())
        line = next(f, '')
    return table, line


def read_table_format_2(f, line, table):
    # declare team name length variable to apply condition to later
    team_name_length = None

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
            table = set_champions_relegation_promotion(table, position, line[goal_data.end():].split())
        line = next(f, '')
    return table, line


def detect_table_format(line):
    if match_table_format_1(line):
        print("Detected table format no. 1.")
        return read_table_format_1
    elif match_table_format_2(line):
        print("Detected table format no. 2.")
        return read_table_format_2
    return None
