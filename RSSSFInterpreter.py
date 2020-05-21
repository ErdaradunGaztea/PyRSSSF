import re

from entities.Teams import Table


def interpret(file):
    with open(file, 'r') as f:
        source = ""
        for count, line in enumerate(f):
            if count == 0:
                source = line.strip()
            # omit lines which don't contain 'Final Table' header
            if line.__contains__('Final Table'):
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
                        split = re.search(r'\s{2,}', next_line)
                        team = next_line[:split.start()]
                        next_line = next_line[split.end():]
                        line_data = next_line.split()
                        goals = line_data[4].split("-")
                        table.add_row(position, team, line_data[1], line_data[2], line_data[3], goals[0], goals[1])
                        if line_data.__contains__('Champions'):
                            table.standings.get(position).set_champions()
                        if line_data.__contains__('Relegated'):
                            table.standings.get(position).set_relegation()
                    next_line = next(f, '')
                return table.add_competitions()
