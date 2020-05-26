from RSSSFInterpreter import interpret
from Spider import run_spider

import os.path


# TODO allow starting after certain header (like '2nd Division')
def main(country, year):
    # will download data only if isn't already downloaded
    if not os.path.isfile("{0}_{1}.txt".format(country, year)):
        run_spider(country, year)
    t, m, s = interpret("{0}_{1}.txt".format(country, year))
    t.to_wiki("{0}_{1}.wiki.txt".format(country, year))
    m.to_wiki("{0}_{1}.wiki.txt".format(country, year))
    s.to_wiki("{0}_{1}.wiki.txt".format(country, year))
    return t, m, s
