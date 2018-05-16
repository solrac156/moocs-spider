# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    stars_number = scrapy.Field()
    last_update = scrapy.Field()
    review_body = scrapy.Field()
    course_stage = scrapy.Field()
    pass
