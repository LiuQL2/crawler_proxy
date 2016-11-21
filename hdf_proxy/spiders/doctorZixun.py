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

    name = 'doctor_zixun'
    allowed_domains = ["haodf.com"]
    start_urls=['http://www.haodf.com/wenda/chenxiannan_g_4491952856.htm?p=1']
    # start_urls=['http://wxinhua.haodf.com/zixun/list.htm',
    #             'http://postone.haodf.com/zixun/list.htm']
    custom_settings = {
        'ITEM_PIPELINES' : {
            # 'yuanyuan.pipelines.ZixunPipeline': 300
        }
    }
    # start_urls = []
    # doctor_url_file = open('/Users/Qianlong/Desktop/eHealth/haodaifu/doctorUrl2.csv', 'r')
    # doctor_url_file = open('./data/doctorUrl.csv', 'r')
    # reader = csv.reader(doctor_url_file)
    # for url in reader:
    #     print '\''+ url[0] + '\','
    #     start_urls.append(url[0])
    # doctor_url_file.close()

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
            print url
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
                if '使用电话咨询服务' in head[0]:
                    print '#####',head[0]
                    order = {}
                    order['doctor_url'] = (sel.xpath('//a[@class="choiced"]/@href').extract()[0]).replace('zixun/list.htm','payment/newintro')
                    # doctor_url = sel.xpath('//a[@class="choiced"]/@href').extract()[0]
                    # print
                    order['page_url'] = response.meta['page_url']
                    order['order_type'] = 'call_consult'
                    order['order_submit_time'] = conversation.xpath('div[3]/table//tr[1]/td[1]/text()').extract()[0]
                    order['order_time'] = conversation.xpath('div[3]/table//tr[1]/td[2]/text()').extract()[0]
                    charge = conversation.xpath('div[3]/table//tr[2]/td[1]/text()').extract()
                    if len(charge) == 0:
                        order['order_charge'] = ''
                    else:
                        order['order_charge'] = charge[0]

                    order['order_state'] = conversation.xpath('div[3]/table//tr[2]/td[2]/text()').extract()[0]
                    disease_content = conversation.xpath('div[3]/table//tr[4]/td')
                    order['order_disease'] = disease_content.xpath('string(.)').extract()[0]
                    item_list.append(order)
                elif '购买了电话问诊' in head[0]:
                    print '#####', head[0]
                    order = {}
                    order['doctor_url'] = (sel.xpath('//a[@class="choiced"]/@href').extract()[0]).replace('zixun/list.htm','payment/newintro')
                    order['page_url'] = response.meta['page_url']
                    order['order_type'] = 'call_ask'
                    order_content = conversation.xpath('div[@class="h_s_cons new-yh-stream"]//div[@class="new-con"]/text()').extract()
                    print ';;;;;',len(order_content)
                    order['order_submit_time'] = None
                    order['order_time'] = order_content[0]
                    order['order_charge'] = conversation.xpath('div[@class="h_s_cons new-yh-stream"]/h3/span/text()').extract()[0]
                    order['order_state'] = order_content[1]
                    order['order_disease'] = order_content[2]
                    item_list.append(order)
        # item = ZixunItem2()
        # item['item_list'] = item_list
        # return item
        csv_file = open('/Users/Qianlong/Desktop/eHealth/haodaifu/data/hdf_zixun_test.csv', 'a+')
        file_writer = csv.writer(csv_file)
        for item in item_list:
            file_writer.writerow([item['doctor_url'],item['page_url'],item['order_type'],item['order_submit_time'],item['order_time'],item['order_charge'],item['order_state'],item['order_disease']])
        csv_file.close()
