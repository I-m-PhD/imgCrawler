# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituItem(scrapy.Item):
    # for sorting
    score = scrapy.Field()
    quantity = scrapy.Field()
    # level-1 folders
    mid = scrapy.Field()
    name = scrapy.Field()
    # for database
    location = scrapy.Field()
    occupation = scrapy.Field()
    age = scrapy.Field()
    birthday = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    bwh = scrapy.Field()  # Bust-Waist-Hip
    introduction = scrapy.Field()
    # level-2 folders
    album_title = scrapy.Field()
    # level-3 images
    img_url = scrapy.Field()

