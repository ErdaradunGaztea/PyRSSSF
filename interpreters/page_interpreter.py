import os.path

from crawling import run_spider
from entities.teams import TeamDictionary
from interpreters.header_detector import HeaderDetector
from interpreters.match_interpreter import MatchInterpreter
from interpreters.table_interpreter import TableInterpreter
from interpreters.topscorer_interpreter import TopscorerInterpreter


class PageInterpreter:
    def __init__(self, country, year):
        self.country = country
        self.year = year
        self.headers = []
        self.interpreters = []
        # TODO: or maybe a dictionary? or a dedicated object that takes wiki section order into consideration?
        self.results = []

    def header(self, header: str):
        self.headers.append(header.lower())
        return self

    def table(self):
        self.interpreters.append(TableInterpreter())
        return self

    def matches(self):
        self.interpreters.append(MatchInterpreter())
        return self

    def topscorers(self):
        self.interpreters.append(TopscorerInterpreter())
        return self

    def run(self):
        TeamDictionary.country = self.country
        file = "{0}_{1}.txt".format(self.country, self.year)
        wiki_file = "{0}_{1}.wiki.txt".format(self.country, self.year)

        # will download data only if isn't already downloaded
        if not os.path.isfile(file):
            run_spider(self.country, self.year)

        with open(file, 'r', encoding='utf-8') as f:
            # read first line with source
            source = next(f, None).strip()

            # find all headers
            for header in self.headers:
                line = next(f, None)
                while line is not None and not line.lower().__contains__(header):
                    line = next(f, None)

            line = next(f, None)
            for interpreter in self.interpreters:
                if line is None:
                    break
                result, line = interpreter.run(f, source)
                self.results.append(result)

        for result in self.results:
            result.to_wiki(wiki_file)

        HeaderDetector.clear()
        return self.results
