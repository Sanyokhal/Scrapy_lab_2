# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Faculty(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class Kafedra(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    faculty = scrapy.Field()
    speciality = scrapy.Field()


class DetailedKafedra(scrapy.Item):
    name = scrapy.Field()
    learn_form = scrapy.Field()
    ects_credits = scrapy.Field()
