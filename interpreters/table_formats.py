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
        r'\s*[0-9]+\s+[\D]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s*[\w\s]*',
        line)


def match_table_format_2(line):
    """
    Example lines:
     1.Besiktas JK Istanbul        30  20  9  1  63-24  69
     1. Þróttur R.           18 12  4  2   40:21     40
    """
    return re.match(
        r'\s*[0-9]+\.\s*[\D]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s*[-:]\s*[0-9]+\s+[0-9]+\s*[\w\s]*',
        line)


# TODO: extract common code
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
                r'([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s*([\w\s]*)',
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
    while line.strip():
        # process the line only if it fits the regex
        if match_table_format_2(line):
            # get position in table
            position_re = re.search(r'\s*([0-9]+)\.', line)
            position = int(position_re.group(1))
            line = line[position_re.end():]
            # find matches, goals and points data
            data = re.search(
                r'([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s*[-:]\s*([0-9]+)\s+([0-9]+)\s+([\w\s]*)',
                line)
            # extract team name and remove additional info in parentheses ()
            team = re.sub(r'\([^)]+\)', '', line[:data.start()]).strip()
            table.add_row(position, team, data.group(2), data.group(3), data.group(4),
                          data.group(5), data.group(6))
            # extract points and any additional notes
            table = set_champions_relegation_promotion(table, position, data.group(8).split())
        line = next(f, '')
    return table, line


def detect_table_format(line):
    if line is not None:
        if match_table_format_1(line):
            print("Detected table format no. 1.")
            return read_table_format_1
        elif match_table_format_2(line):
            print("Detected table format no. 2.")
            return read_table_format_2
    return None
