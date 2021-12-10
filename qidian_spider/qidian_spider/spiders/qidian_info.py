import os.path
import re

import scrapy
from bs4 import BeautifulSoup
from urllib import parse
from ..items import QidianInfoSpiderItem, QidianTypeSpiderItem, QidianBookMsgSpiderItem, QidianBookChapterMsgSpiderItem
import time
from scrapy.http import Request


class QidianInfoSpider(scrapy.Spider):
    name = 'qidian_info'
    allowed_domains = ['qidian.com']
    start_urls = ['http://www.qidian.com/']

    def parse(self, response):
        # 解析起点中文网的首页部分, 解析出不同的分类以及不同分类下的url, title, text, count
        bs_obj = BeautifulSoup(response.body, "lxml")
        div_obj = bs_obj.find('div', {
            "class": "classify-list fl so-awesome"
        })
        dd_list = div_obj.find_all('dd')
        base_url = self.start_urls[0]
        items = QidianInfoSpiderItem()
        self.log("页面解析中.............")
        for dd_obj in dd_list:
            a_obj = dd_obj.a
            items["info_type_text"] = a_obj.i.text
            items["info_type_url"] = parse.urljoin(base_url, a_obj.get("href"))
            items["info_type_title"] = a_obj.get("title")
            items["info_type_count"] = a_obj.b.text
            items["spider_name"] = self.name
            items["spider_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield items
            yield Request(
                url=items["info_type_url"],
                callback=self.parse_type,
                meta={"info_type_text": items["info_type_text"]}
            )

    def parse_type(self, response):
        info_type_text = response.meta["info_type_text"]
        self.log("parase_type is called......")
        items = QidianTypeSpiderItem()
        bs_obj = BeautifulSoup(response.body, "lxml")
        div_obj = bs_obj.find('div', {
            "class": "sub-type-wrap"
        })
        if div_obj is None:
            div_obj = bs_obj.find('div', {
                "class": "main-nav-wrap"
            })
        a_list_sim_type = div_obj.find_all('a')
        for a_sim_type in a_list_sim_type:
            items["info_type_text"] = info_type_text
            items["type_title"] = a_sim_type.text
            items["type_url"] = parse.urljoin('https:', a_sim_type.get("href"))
            yield items
            yield Request(
                url=items["type_url"],
                callback=self.parse_book_msg,
                meta={"type_title": items["type_title"]}
            )

    def parse_book_msg(self, response):
        type_title = response.meta["type_title"]
        self.log("parase_book_msg is called...")
        items = QidianBookMsgSpiderItem()
        bs_obj = BeautifulSoup(response.body, "lxml")
        div_obj_list = bs_obj.find_all('div', {
            "class": "book-mid-info"
        })
        for div_obj in div_obj_list:
            items["type_title"] = type_title
            items["book_name"] = div_obj.find('a', {
                "data-eid": "qd_B58"
            }).text
            items["book_url"] = parse.urljoin('https:',
                                              div_obj.find('a', {
                                                  "data-eid": "qd_B58"
                                              }).get("href")
                                              )
            items["book_count"] = div_obj.find('p', {
                "class": "update"
            }).span.span.text.encode("utf-8").decode("utf-8")
            items["author_name"] = div_obj.find('a', {
                "data-eid": "qd_B59"
            }).text
            items["book_classifi"] = div_obj.find('a', {
                "data-eid": "qd_B60"
            }).text + "|" + div_obj.find('a', {
                "data-eid": "qd_B61"
            }).text
            items["book_description"] = div_obj.find('p', {
                "class": "intro"
            }).text
            items["book_status"] = div_obj.find('p', {
                "class": "author"
            }).find('span').text
            yield items
        book_url_with_catalog = parse.urljoin(items["book_url"], "#Catalog")
        yield Request(url=parse.urljoin("https:", book_url_with_catalog), callback=self.parase_book_content,
                      meta={"book_name": items["book_name"]})
        # 获取下一个页面的链接
        nextl = bs_obj.find('a', {
            "class": "lbf-pagination-next"
        }).get("href")
        if nextl != ("javascript:;"):
            next_url = parse.urljoin('https:', nextl)
            yield Request(url=next_url, priority=100, callback=self.parse_book_msg, meta={"type_title": type_title})

    def parase_book_content(self, response):
        items = QidianBookChapterMsgSpiderItem()
        # 书名
        items["book_name"] = response.meta["book_name"]
        bs_obj = BeautifulSoup(response.body, "lxml")
        volums_obj = bs_obj.find_all('div', {
            "class": "volume",

        })
        for volum_obj in volums_obj:
            # 卷名
            items["volum_name"] = volum_obj.find('h3').text
            # 第一个章节名
            chapters_obj_1_volum = volum_obj.find_all('h2', {
                "class": "book_name"
            })
            for chapters_obj in chapters_obj_1_volum:
                items["chapters_name"] = chapters_obj.text
                # fixme(下面两个属性没有获取到,需要进一步查看原因)
                items["chapters_url"] = parse.urljoin("http:", chapters_obj.get("href"))
                items["chapters_msg"] = chapters_obj.get("alt")
                yield items
