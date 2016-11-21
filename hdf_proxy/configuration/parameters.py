# -*- coding:utf-8 -*-

# 项目的参数配置，包括数据库表（表名、属性名、主键）、维护人员邮箱、需要访问的网站首页以及被封的状态；
# 如果没有参数没有，比如没有数据库

# 工作人员邮箱，以字典的形式保存，且字典中根据工作人员的工作以list的形式出现
STAFF_MAIL = dict(
    proxy_staff_list = [
        'LiuQL2@qq.com',
    ],
    spider_staff_list = [
        'LiuQL2@163.com',
    ],
)

# 设置用来发邮件的邮箱
SENDER_MAIL = dict(
    host = 'smtp.163.com',#邮箱服务器
    port = 465,#服务器端口，SSL的为465，一般的为25
    user = 'LiuQL2@163.com',#邮箱地址
    password = 'SWLdwh2',#邮箱密码
    sent_from = 'Haodf Python Spider',#显示的发件人名称
)


# 改项目爬虫需要爬取的网站，写出网站首页，同时给出如果ip被封在网页源代码中出现的唯一字段，
# 如好大夫出现的字段如下。
WEBSITE = dict(
    home_page = 'http://wxinhua.haodf.com/zixun/list.htm',#需要抓取的网站首页网址
    forbidden = '<title>250 Forbidden</title>',#ip被封后源代码中出现的字段
)




# 数据库信息配置，这里用于连接数据库，各个属性是否必需如下
DATABASE_INFO = dict(
    host='localhost',#数据库所在主机，必需
    user='root',#用户名，必需
    passwd='962182',#用户密码，必需
    database='hdf',#数据库名称，必需
    port=3306,#端口号，必需
    charset='utf8',#数据库编码方式，必需
    use_unicode = True,
)




# 数据库表的配置，每一个表都要添加一个dict，如下面的PROXY_TABLE，column是属性名，primary_key是主键
# 一个数据表添加完成之后在DATAB_TABLES里面添加，如'proxy'是数据库中真实的表名，将其对应到PROXY_TABLE。
PROXY_TABLE = dict(
    name = 'proxy',#存储ip代理的数据库表的名称，必需。
    proxy_status = 'proxy_status',#显示代理是否可用的字段，'True'表示可用，'False'表示不可用，必需.
    proxy_useful = 'True',#可用的状态，本例中为字符串True。
    primary_key = ['proxy_ip'],#定义主键，这个表中在数据库中没有设置主键，不过ip能唯一表识一个记录，必需.
    column = [
        'proxy_domain',#代理域名
        'proxy_ip',#代理IP
        'proxy_port',#代理端口
        'proxy_type',#协议类型，http或者https
        'proxy_pwd',#代理密码
        'proxy_status',#代理状态，是否能用
        'proxy_add_date',#添加日期
        'proxy_days',#可用天数
        'proxy_address',#服务器地理位置
    ],
)

DATABASE_TABLES = dict(
    proxy = PROXY_TABLE,#将proxy与proxy_table对应，这里的'proxy'是数据库中真实存在的表名，并且表的结构就是上面定义的方式
    proxy_table_name = 'proxy',#用户存储ip代理的表的名称。
)


