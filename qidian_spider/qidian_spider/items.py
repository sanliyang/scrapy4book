# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianInfoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    info_type_text = scrapy.Field()
    info_type_title = scrapy.Field()
    info_type_url = scrapy.Field()
    info_type_count = scrapy.Field()
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()


class QidianTypeSpiderItem(scrapy.Item):
    info_type_text = scrapy.Field()
    type_title = scrapy.Field()
    type_url = scrapy.Field()


class QidianBookMsgSpiderItem(scrapy.Item):
    type_title = scrapy.Field()
    book_url = scrapy.Field()
    book_name = scrapy.Field()
    book_count = scrapy.Field()
    author_name = scrapy.Field()
    book_classifi = scrapy.Field()
    book_description = scrapy.Field()
    book_status = scrapy.Field()


class QidianBookChapterMsgSpiderItem(scrapy.Item):
    book_name = scrapy.Field()
    volum_name = scrapy.Field()
    chapters_name = scrapy.Field()
    chapters_url = scrapy.Field()
    chapters_msg = scrapy.Field()
