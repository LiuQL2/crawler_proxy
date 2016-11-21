#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 用来发送邮件的类.
这个类继承类SMTP_SSL，主要用于带有SSL加密方式的服务器。
在使用类的过程中需按照如下步骤进行：
mail = MialClass()
mail.connect_server()
mail.login_server()
mail.send_mail(to_addrs_list, content, subject)
mail.quit_server()

If there anything do not understand, see stmplib for details.
'''

# Author: Liu Qianlong <LiuQL2@163.com>
# Date: 2016.10.05


import smtplib
from email.mime.text import MIMEText
from email.header import Header
import socket
from hdf_proxy.configuration.parameters import SENDER_MAIL


class MailClass(smtplib.SMTP_SSL):

    def __init__(self, host='', port=0, local_hostname=None,keyfile=None, certfile=None,timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """初始化一个新的实例.
        这里对服务器的连接、登陆的用户等都是在parameters里面进行配置的。
        因为这个类继承smtplib.SMTP_SSL，为了避免后续会出现变量不存在的问题，所以这里初始化和SMTP_SSL的一样
        只是为了自己实用的方便在最后新建类一个self.server
        """
        self.keyfile = keyfile
        self.certfile = certfile
        smtplib.SMTP.__init__(self, host, port, local_hostname, timeout)
        self.server = smtplib.SMTP_SSL()



    def connect_server(self):
        """连接服务器，参数在parameters配置，这里调用。
        :return: 无返回内容
        """
        self.server.set_debuglevel(1)#在接下来发邮件的过程中输出所有的状态。
        self.server.connect(host = SENDER_MAIL['host'], port = SENDER_MAIL['port'])#连接服务器，域名端口等直接调用。


    def login_server(self):
        """
        登陆用户
        :return: 无返回内容。
        """
        self.server.helo()#服务器与本机之间进行通信确认
        self.server.ehlo()
        self.server.ehlo_or_helo_if_needed()
        self.server.login(user=SENDER_MAIL['user'], password=SENDER_MAIL['password'])#登陆

    def send_mail(self,to_addrs_list = None, content = None, subject = None):
        """发送邮件，功能设计的只能发送纯文本的邮件内容
        :param to_addrs_list: 需要发给的地址，是一个list，每一个邮箱地址是list的一个元素。
        :param content: 邮件的内容，是一个string。
        :param subject: 邮件的主题。
        :return: 无返回内容。
        """
        if to_addrs_list != None:
            to_addrs_str = to_addrs_list[0]
            for index in range(1, len(to_addrs_list),1):
                to_addrs_str = to_addrs_str + ',' + to_addrs_list[index]
            to_addrs = list([to_addrs_str])
        else:
            print 'no Email address to send to!'
            raise smtplib.SMTPException()

        if content != None:
            msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                % (SENDER_MAIL['sent_from'], ", ".join(to_addrs), subject))
            msg = msg + content
            self.server.sendmail(from_addr=SENDER_MAIL['user'],to_addrs=to_addrs,msg=msg)
        else:
            print 'No content in the email!'
            raise smtplib.SMTPException()

    def quit_server(self):
        """退出登陆
        :return: 无返回内容
        """
        self.server.quit()

    def close_server(self):
        """
        关闭连接。
        :return: 无返回内容。
        """
        self.server.close()