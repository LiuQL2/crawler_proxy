# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from settings import database_info

#保存proxy到数据库中
class GetProxyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):

        conn.execute("SET NAMES utf8")
        for index in range(0, len(item['proxy_ip']), 1):
            # cursor.execute('select * from proxy_effective where proxy_ip = %s and proxy_port = %s', [proxy[1],proxy[2]])

            conn.execute("select proxy_ip from proxy_all where proxy_ip = '%s' " % item['proxy_ip'][index])
            # conn.execute("select proxy_ip from proxy_all where proxy_ip = '%s' and proxy_port = '%s'" % (item['proxy_ip'][index], item['proxy_port'][index]])
            # conn.execute("""
            #         insert into proxy_all(proxy_ip, proxy_port, proxy_type, proxy_location,proxy_speed)
            #         values(%s, %s, %s, %s, %s)""",
            #         (item["proxy_ip"][index], item["proxy_port"][index], item["proxy_type"][index], item["proxy_location"][index],item["proxy_speed"][index]))
            ret = conn.fetchone()
            if ret:
                pass
            else:
                conn.execute("""
                    insert into proxy_all(proxy_ip, proxy_port, proxy_type, proxy_location,proxy_speed)
                    values(%s, %s, %s, %s, %s)""",
                    (item["proxy_ip"][index], item["proxy_port"][index], item["proxy_type"][index], item["proxy_location"][index],item["proxy_speed"][index]))