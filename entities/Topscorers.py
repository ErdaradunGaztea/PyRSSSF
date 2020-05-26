class Topscorer:
    def __init__(self, name, goals, team=None, country_code=None):
        self.name = name
        self.goals = goals
        self.team = team
        self.country_code = country_code

    def to_wiki(self, top=False):
        return "|{{{{flaga|{3}}}}} {2}[[{0}]]{2}\n" \
               "|{2}{{{{Fb team {1}}}}}{2}\n" \
               "|".format(self.name, self.team.fb if self.team.fb else "brak", "'''" if top else "",
                          self.country_code if self.country_code else "")


class TopscorerTable:
    def __init__(self):
        self.scorers = []

    def add_topscorer(self, name, goals, team=None, country_code=None):
        self.scorers.append(Topscorer(name, goals, team, country_code))

    def to_wiki(self, filename):
        # first, sort scorers in-place
        self.scorers.sort(key=lambda s: s.goals, reverse=True)

        # gather info about consecutive scorers with same number of goals
        scorer_goals = dict()
        for scorer in self.scorers:
            if not scorer_goals.__contains__(scorer.goals):
                scorer_goals[scorer.goals] = 1
            else:
                scorer_goals[scorer.goals] += 1

        with open(filename, 'a+', encoding='utf-8') as f:
            # header
            f.write("== Najlepsi strzelcy ==\n")
            f.write("{| class=\"wikitable\"\n!Bramki\n!width=240|Strzelcy\n!width=200|Drużyna\n|-\n")

            position = 0
            # for each goal score descending
            for index, goals in enumerate(sorted(scorer_goals.keys(), reverse=True)):
                f.write("|rowspan={1} style=\"text-align: center\"| {2}{0}{2} {{{{gol}}}}\n".format(
                    goals, scorer_goals[goals], "'''" if index == 0 else "")
                )
                # for each player with this score
                for i in range(scorer_goals[goals]):
                    f.write(self.scorers[position].to_wiki(index == 0))
                    # select proper line ending if player is last in the table
                    f.write("}\n" if position == len(self.scorers) - 1 else "-\n")
                    position += 1
