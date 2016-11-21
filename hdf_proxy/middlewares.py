# -*- coding: utf-8 -*-
import random
import base64
# from settings import PROXIES
from hdf_proxy.classes.proxyClass import ProxyClass


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        user_agent = random.choice(self.agents)
        print user_agent
        request.headers.setdefault('User-Agent', user_agent)


class ProxyMiddleware(object):
    def process_request(self, request, spider):


        request.meta['proxy'] = "http://182.254.139.66:3128"#lql tencent,beijing,can
        # request.meta['proxy'] = "http://23.106.159.52:3128"#LiuQL US
        # request.meta['proxy'] = "http://123.206.7.172:3128"#LiuQL tencent,shanghai
        # proxy_user_pass = "longer:longer"
        proxy_user_pass = "ehealth:longer"
        encoded_user_pass = base64.b64encode(proxy_user_pass)
        print encoded_user_pass
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass



        # proxy_instance = ProxyClass()
        # proxy_tuple = proxy_instance.select_proxy(table='proxy')
        # print '*********',type(proxy_tuple),len(proxy_tuple)
        # proxy_instance.colse_connect()
        #
        # if len(proxy_tuple) >= 1:
        #     proxy = random.choice(proxy_tuple)
        #     print type(proxy), proxy
        #     request.meta['proxy'] = proxy[3].lower()+'://' + proxy[1] + ':' + proxy[2]
        #     # request.meta['proxy'] = "http://119.29.234.174:3128"#sww tencent
        #     # request.meta['proxy'] = "http://23.106.159.52:3128"#LiuQL US
        #     # request.meta['proxy'] = "http://182.254.139.66:3128"#LiuQL tencent
        #
        #     #如果代理需要密码可以这样设置
        #     # proxy_user_pass = "ehealth:longer"
        #     # proxy_user_pass = "longer:longer"
        #     proxy_user_pass = proxy[9]+':' + proxy[4]
        #     # setup basic authentication for the proxy
        #     encoded_user_pass = base64.b64encode(proxy_user_pass)
        #     print encoded_user_pass
        #     request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        # else:
        #     pass