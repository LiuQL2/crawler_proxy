#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 对代理IP进行维护。
'''

# Author: Liu Qianlong <LiuQL2@163.com>
# Date: 2016.10.17

import MySQLdb
import os
import sys
import MySQLdb.cursors
import urllib2
import time
from hdf_proxy.configuration.parameters import PROXY_TABLE as proxy_table
from hdf_proxy.classes.databaseOperationClass import DatabaseOperationClass
from hdf_proxy.settings import USER_AGENTS as user_agents
reload(sys)
sys.setdefaultencoding('utf-8')

class ProxyClass(DatabaseOperationClass):

    def maintain_proxy(self):
        try:
            proxy_list = self.select(table = proxy_table['name'])
            for proxy in proxy_list:
                if self.ping_ip(proxy) and self.verify_ip_hdf(proxy):
                    pass
                else:
                    self.delete_proxy(table='proxy_effective', proxy=proxy)
                    self.delete_proxy(table='proxy_all', proxy=proxy)
            self._maintain_effective_process = 'over'
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])



    #ping功能，验证代理ip是否可用
    def verify_ping(self,proxy=None):
        ip = proxy[1]
        ping_cmd = 'ping -c 5 -W 0.005 %s' % ip
        ping_result = os.popen(ping_cmd).read()
        # print 'ping_cmd : %s, ping_result : %r' % (ping_cmd, ping_result)
        if 'received, 0.0% packet loss' in ping_result:
            # print 'ping %s ok' % ip
            return True
        else:
            # print 'ping %s fail' % ip
            return False

    #验证一个代理是否能够访问好大夫
    def verify_website(self, proxy_dict):
        proxy_temp = urllib2.ProxyHandler({proxy['proxy_type'].lower(): proxy['proxy_ip'] + proxy['proxy_port']})

        opener = urllib2.build_opener(proxy_temp)
        urllib2.install_opener(opener)
        try:
            response = urllib2.urlopen('http://www.haodf.com')
            sel = response.read()
            if '<title>250 Forbidden</title>' not in sel:
                return True
            else:
                return False
        except Exception,e:
            return False


if __name__ == '__main__':
    proxy = ProxyClass()
    proxy.maintain_effective()
    proxy.all_to_effective()
    proxy.colse_connect()