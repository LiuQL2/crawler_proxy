# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetProxyItem(scrapy.Item):
    proxy_ip = scrapy.Field()
    proxy_port = scrapy.Field()
    proxy_location = scrapy.Field()
    proxy_speed = scrapy.Field()
    proxy_type = scrapy.Field()

