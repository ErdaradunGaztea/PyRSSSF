import csv


class Team:
    def __init__(self, fb):
        self.fb = fb


class TeamDictionary:
    country = None
    teams = dict()
    with open("teams.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            # outer dictionary has country key
            if not teams.__contains__(line[0]):
                teams[line[0]] = dict()
            teams[line[0]][line[1]] = Team(line[2])

    @staticmethod
    def get(team):
        if not TeamDictionary.teams.__contains__(TeamDictionary.country):
            TeamDictionary.teams.__setitem__(TeamDictionary.country, dict())
        while not TeamDictionary.teams.get(TeamDictionary.country).__contains__(team):
            decision = input('Missing entry for {0}.\n'
                             'Type "1" to associate with other entry.\n'
                             'Type "2" to provide new fb name.\n'
                             'Type "3" to assign temporary fb name (use for entries with typos).\n'
                             'Type "0" to skip this line.'.format(team))
            if decision == '1':
                key = input('Provide key of the other entry to associate with.')
                if TeamDictionary.teams.get(TeamDictionary.country).__contains__(key):
                    TeamDictionary.teams.get(TeamDictionary.country).__setitem__(
                        team, TeamDictionary.teams.get(TeamDictionary.country).get(key))
                    with open("teams.csv", 'a+', encoding='utf-8') as f:
                        f.write("{0},{1},{2}\n".format(
                            TeamDictionary.country,
                            team,
                            TeamDictionary.teams.get(TeamDictionary.country).get(key).fb)
                        )
                else:
                    print('Key doesn\'t exist!')
            elif decision == '2':
                fb_name = input('Provide fb name for new team.')
                TeamDictionary.teams.get(TeamDictionary.country).__setitem__(team, Team(fb_name))
                with open("teams.csv", 'a+', encoding='utf-8') as f:
                    f.write("{0},{1},{2}\n".format(TeamDictionary.country, team, fb_name))
            elif decision == '3':
                fb_name = input('Provide fb name for this entry.')
                TeamDictionary.teams.get(TeamDictionary.country).__setitem__(team, Team(fb_name))
            elif decision == '0':
                return None
        return TeamDictionary.teams.get(TeamDictionary.country).get(team)

