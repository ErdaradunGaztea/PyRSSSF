from rsssf.RSSSFInterpreter_topscorers import read_topscorers


def interpret(file):
    table_header = "final table".lower()
    with open(file, 'r', encoding='utf-8') as f:
        # read first line with source
        source = next(f, None).strip()

        # find table header
        line = next(f, None)
        while line is not None and not line.lower().__contains__(table_header):
            line = next(f, None)

        # TODO: avoid fixed order, sometimes topscorers are above the list of matches
        table = read_table(f, source)
        update_table(table)
        if input("If there isn't anything more than a table, enter 'stop'.") == 'stop':
            return table, None, None
        matches, line = read_matches(f, source)
        topscorers = read_topscorers(f, line)

    return table, matches, topscorers
