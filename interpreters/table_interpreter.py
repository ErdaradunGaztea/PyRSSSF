from entities.teams import Table
from interpreters.table_formats import detect_table_format


class TableInterpreter:
    def __init__(self):
        self.table = None

    def __read_table(self, f, source):
        # create standings table
        print("### Creating table...")
        points_per_win = int(input('How many points per win were awarded?'))
        self.table = Table(source, points_per_win)

        # first strip all empty lines
        line = next(f, '')
        table_format_func = detect_table_format(line)
        while not table_format_func:
            line = next(f, '')
            table_format_func = detect_table_format(line)

        self.table, line = table_format_func(f, line, self.table)
        return line

    def __update_table(self):
        # fill result table with additional info
        menu_prompt = "Table enhancements available:\n" \
                      "* press 1 to add promotions to higher league\n" \
                      "* press 2 to add relegations to lower league\n" \
                      "* press 3 to add qualifications to international competitions\n" \
                      "Leave empty to finalize table creation."
        menu_choice = input(menu_prompt)
        while menu_choice:
            if menu_choice == '1':
                self.table.add_promotions()
            if menu_choice == '2':
                self.table.add_relegations()
            if menu_choice == '3':
                self.table.add_competitions()
            menu_choice = input(menu_prompt)

    def run(self, f, source):
        line = self.__read_table(f, source)
        self.__update_table()
        return self.table, line
