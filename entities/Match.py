from entities.Teams import team_dictionary


class Match:
    def __init__(self, home, away, goals_h, goals_a):
        self.home = team_dictionary.get(home)
        self.away = team_dictionary.get(away)
        self.goals_h = goals_h
        self.goals_a = goals_a

    def to_wiki(self):
        return "<!-- {0:>25} --> {{{{fb r |gf={1}|ga={2}}}}}\n".format(self.away.fb, self.goals_h, self.goals_a)


class BlankMatch:
    def __init__(self, team):
        self.home = team
        self.away = team

    def to_wiki(self):
        return "<!-- {0:>25} --> {{{{fb r |r=null}}}}\n".format(self.away.fb)


class MatchRow:
    def __init__(self, home):
        self.home = home
        # creates empty match to place on the diagonal
        # not the best solution, but works and is simple
        self.matches = [BlankMatch(home)]

    def add_match(self, match):
        self.matches.append(match)

    def to_wiki(self, f):
        f.write("{{{{fb r team |t={0}}}}}\n".format(self.home.fb))
        for match in sorted(self.matches, key=lambda m: m.away.fb):
            f.write(match.to_wiki())
        f.write("\n")


class MatchTable:
    def __init__(self, source):
        self.source = source
        self.rows = dict()

    def add_match(self, match):
        home = match.home
        if not self.rows.__contains__(home):
            self.rows.__setitem__(home, MatchRow(home))
        self.rows.get(home).add_match(match)

    def to_wiki(self, filename):
        with open(filename, 'a+', encoding='utf-8') as f:
            # header
            f.write("== Wyniki ==\n")
            f.write("{{{{fb r2 header |nt={0}".format(len(self.rows)))
            for row_key in sorted(self.rows.keys(), key=lambda k: k.fb):
                f.write(" |{0}".format(row_key.fb))
            f.write("}}\n\n")
            # body
            for row_key in sorted(self.rows.keys(), key=lambda k: k.fb):
                self.rows.get(row_key).to_wiki(f)
            f.write("{{{{fb r footer |s=[{0}] {{{{lang|en}}}} }}}}\n\n".format(self.source))