#coding:utf-8

import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import math
import random
import csv
import sys
import urllib2
from hdf_proxy.items import GetProxyItem
from hdf_proxy.pipelines import GetProxyPipeline
reload(sys)
sys.setdefaultencoding('utf-8')


class GetProxySpider(Spider):
    name = 'get_proxy'
    allowed_domains = ["kuaidaili.com"]
    # start_urls = ['http://www.kuaidaili.com/free/inha/2/']
    custom_settings = {
        'ITEM_PIPELINES' : {
            'hdf_proxy.pipelines.GetProxyPipeline': 300
        }
    }
    start_urls = []
    for index in range(1, 1000, 1):
        in_url = 'http://www.kuaidaili.com/free/inha/' + str(index) + '/'
        out_url = 'http://www.kuaidaili.com/free/outha/' + str(index) + '/'
        start_urls.append(in_url)
        start_urls.append(out_url)

    def make_requests_from_url(self, url):
        return Request(url = url)

    def parse(self, response):
        sel = Selector(response)
        item = GetProxyItem()
        item['proxy_ip'] = sel.xpath('//table//tr/td[@data-title="IP"]/text()').extract()
        item['proxy_port'] = sel.xpath('//table//tr/td[@data-title="PORT"]/text()').extract()
        item['proxy_location'] = sel.xpath('//table//tr/td[5]/text()').extract()
        item['proxy_type'] = sel.xpath('//table//tr/td[4]/text()').extract()
        item['proxy_speed'] = sel.xpath('//table//tr/td[6]/text()').extract()
        print 'return item'
        return item
