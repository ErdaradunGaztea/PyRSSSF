import scrapy
from scrapy.crawler import CrawlerProcess


class RSSSFSpider(scrapy.Spider):
    name = "RSSSF_default_spider"

    def __init__(self, country, year, **kwargs):
        super().__init__(**kwargs)
        self.country = country
        self.year = year
        self.start_url = ['http://www.rsssf.com/tables{0}/{1}{2}.html'.format(country[0], country, year),
                          'http://www.rsssf.com/tables{0}/{1}{2}.html'.format(country[0], country, str(year)[-2:])]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open("temp", "w", encoding='utf-8') as text_file:
            text_file.write(response.css('body > pre::text').get())
        with open("{0}_{1}.txt".format(self.country, self.year), "w", encoding='utf-8') as text_file:
            with open("temp", "r", encoding='utf-8') as f:
                text_file.write(response.url + "\n")
                for count, line in enumerate(f):
                    if count % 2 == 0:
                        text_file.write(line)


def run_spider(country, year):
    process = CrawlerProcess()
    process.crawl(RSSSFSpider, country=country, year=year)
    process.start()

# scrapy runspider Spider.py
