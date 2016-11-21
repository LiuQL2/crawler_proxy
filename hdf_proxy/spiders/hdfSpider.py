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
reload(sys)
sys.setdefaultencoding('utf-8')


class DoctorZixunSpider(Spider):

    name = 'recipe'
    allowed_domains = ["haodf.com"]
    start_urls=['http://wxinhua.haodf.com/zixun/list.htm',
                ]
    custom_settings = {
        'ITEM_PIPELINES' : {
            # 'yuanyuan.pipelines.RecipePipeline': 300
        }
    }


    def make_requests_from_url(self, url):
        return Request(url = url)

    def parse(self, response):
        sel = Selector(response)
        page_number_content = sel.xpath('//div[@class="page_turn"]/a[@rel="true"][2]/text()').extract()
        if len(page_number_content) == 1:
            mode = re.compile(r'\d+')
            page_number = int(mode.findall(page_number_content[0])[0]) + 1
        else:
            page_number = 2

        # url_format = sel.xpath('//ul[@class="clearfix f16"]/li[1]/a/@href').extract()[0] + 'zixun/list.htm?type=&p='
        url_format = sel.xpath('//a[@class="choiced"]/@href').extract()[0] + '?type=&p='
        for index in range(1, page_number,1):
            url = url_format + str(index)
            print '*****',url
            yield Request(url, callback =self.get_phone_zixun_url)

    #在医生的患者服务区中找出所有的电话咨询的url
    def get_phone_zixun_url(self,response):
        sel = Selector(response)
        zixun_list_content = sel.xpath('//div[@class="zixun_list"]//tr/td[3]/p')
        # print len(zixun_list_content)
        for zixun in zixun_list_content:
            img_title_list = zixun.xpath('img/@title').extract()
            if '电话咨询' in img_title_list:
                zi_xun_page_url = zixun.xpath('a/@href').extract()[0]
                # print '&&&&&', zi_xun_page_url
                yield Request(url=zi_xun_page_url, meta={'page_url':zi_xun_page_url}, callback=self.get_zixun_pages)

    #在一个进行电话咨询的患者中找出该患者与医生对话的每一个页面url
    def get_zixun_pages(self,response):
        sel = Selector(response)
        page_number_content = sel.xpath('//div[@class="page_turn"]/a[@class="page_turn_a"][last()]/text()').extract()
        if len(page_number_content) != 0:
            mode = re.compile(r'\d+')
            page_number = int(mode.findall(page_number_content[0])[0]) + 1
        else:
            page_number = 2
        url_format = response.meta['page_url']
        for index in range(1, page_number,1):
            url = url_format + '?p=' + str(index)
            # print '一个患者与医生的对话',url
            yield Request(url, meta={'page_url':url_format}, callback=self.get_zixun_info)

    #抓取电话咨询的内容
    def get_zixun_info(self,response):
        sel = Selector(response)
        conversation_list_content = sel.xpath('//div[@class="zzx_yh_stream"]/div[@class="stream_yh_right"]')
        item_list = []
        for conversation in conversation_list_content:
            head = conversation.xpath('div[3]//h3/text()').extract()
            if len(head) != 0:
                print head[0]