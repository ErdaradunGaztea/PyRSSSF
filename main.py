from RSSSFInterpreter import interpret
from Spider import run_spider


def main(country, year):
    run_spider(country, year)
    t = interpret("{0}_{1}.txt".format(country, year))
    t.to_wiki("{0}_{1}.wiki.txt".format(country, year))
    return t
