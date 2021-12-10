#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time :2021/12/8 11:44
# @Author : liby
# @File: run.py
# @Software : PyCharm
from scrapy import cmdline


name = 'qidian_info'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())