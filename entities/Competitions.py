import csv


class Competition:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class CompetitionInstance:
    def __init__(self, competition):
        self.competition = competition
        self.season = None
        self.round = None
        self.note = None

    def get_color(self):
        return self.competition.color

    def get_name(self):
        return self.competition.name


class CompetitionDictionary:
    def __init__(self):
        self.competitions = dict()

    def get(self, competition):
        while not self.competitions.__contains__(competition):
            c_name = input('Missing entry. You have to create new competition. Provide competition name.')
            c_color = input('Provide color. Leave empty if not applicable.')
            c = Competition(c_name, c_color)
            self.competitions.__setitem__(competition, c)
            with open("competitions.csv", 'a+', encoding='utf-8') as f:
                f.write("{0},{1},{2}\n".format(competition, c_name, c_color))
        return self.competitions.get(competition)


competition_dictionary = CompetitionDictionary()
d = dict()
with open("competitions.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for line in reader:
        d[line[0]] = Competition(line[1], line[2])
competition_dictionary.competitions = d
