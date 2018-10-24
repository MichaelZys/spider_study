# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_id=scrapy.Field()
    book_name=scrapy.Field()
    book_type = scrapy.Field()
    book_author=scrapy.Field()
    last_update_time=scrapy.Field()
    book_introduce=scrapy.Field()
    book_chapter=scrapy.Field()
    book_content=scrapy.Field()
    book_content_url=scrapy.Field()
