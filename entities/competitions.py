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

    def to_wiki(self, rows, num_note):
        return "{{{{Fb cl2 qr |rows={0:<2}|s={1} |c={2} |r={3} {4}}}}}\n".format(
            rows, self.season, self.get_name(), self.round, "|nt={0}".format(num_note) if self.note else ""
        )


class CompetitionDictionary:
    competitions = dict()
    with open("competitions.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            competitions[line[0]] = Competition(line[1], line[2])

    @staticmethod
    def get(competition):
        while not CompetitionDictionary.competitions.__contains__(competition):
            c_name = input('Missing entry. You have to create new competition. Provide competition name.')
            c_color = input('Provide color. Leave empty if not applicable.')
            c = Competition(c_name, c_color)
            CompetitionDictionary.competitions.__setitem__(competition, c)
            with open("competitions.csv", 'a+', encoding='utf-8') as f:
                f.write("{0},{1},{2}\n".format(competition, c_name, c_color))
        return CompetitionDictionary.competitions.get(competition)


class LeagueChange:
    def __init__(self, league, season, note=None):
        self.league = league
        self.season = season
        self.note = note

    def get_color(self):
        return "#FFFFFF"

    def to_wiki(self, rows, num_note, event_type):
        return "{{{{Fb cl2 qr |{0}=y |rows={1} |s={2} |c={3} {4}}}}}\n".format(
            event_type, rows, self.season, self.league, "|nt={0}".format(num_note) if self.note else ""
        )


class Relegation(LeagueChange):
    def __init__(self, league, season, note=None):
        super().__init__(league, season, note)

    def get_color(self):
        return "#FFCCCC"

    def to_wiki(self, rows, num_note, event_type):
        return super().to_wiki(rows, num_note, "relegation")


class Promotion(LeagueChange):
    def __init__(self, league, season, note=None):
        super().__init__(league, season, note)

    def get_color(self):
        return "#D0F0C0"

    def to_wiki(self, rows, num_note):
        return super().to_wiki(rows, num_note, "promotion")
