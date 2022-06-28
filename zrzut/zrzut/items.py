# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Zrzuta(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    zebrano = scrapy.Field()
    url = scrapy.Field()
    profil = scrapy.Field()
    img_url = scrapy.Field()
    cel = scrapy.Field()
    wspiera = scrapy.Field()
    fb_shares = scrapy.Field()
    title = scrapy.Field()
    opis = scrapy.Field()