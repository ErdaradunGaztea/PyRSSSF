from entities.topscorers import TopscorerTable
from interpreters.topscorer_formats import detect_topscorer_format


class TopscorerInterpreter:
    def __init__(self):
        self.topscorers = None

    def __read_topscorers(self, f, source):
        print("### Creating topscorers table...")
        self.topscorers = TopscorerTable()

        # first detect topscorer format
        line = next(f, None)
        topscorer_format_func = detect_topscorer_format(line)
        while line is not None and not topscorer_format_func:
            line = next(f, None)
            topscorer_format_func = detect_topscorer_format(line)

        # extract topscorers
        current_goals = 0
        default_country = input("What is the 3-letter code of the default nationality of topscorers?")
        while line is not None and line.strip():
            player, current_goals = topscorer_format_func(line, current_goals, default_country)

            if player:
                self.topscorers.add_topscorer(player)
            line = next(f, None)
        return line

    def run(self, f, source):
        line = self.__read_topscorers(f, source)
        return self.topscorers, line
