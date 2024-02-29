import scrapy
from bs4 import BeautifulSoup


class KarazinSpider(scrapy.Spider):
    name = "karazin"
    allowed_domains = ["start.karazin.ua"]
    start_urls = ["https://start.karazin.ua/programs"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        faculties = soup.find('ul', {'class': 'specialitys'}).find_all('a', {'class': 'flex-item'})
