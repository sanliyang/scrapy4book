import scrapy
from bs4 import BeautifulSoup
from urllib import parse
from ..items import QidianInfoSpiderItem, QidianTypeSpiderItem
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
            yield Request(url=items["info_type_url"], callback=self.parse_type, meta={"info_type_text": items["info_type_text"]})

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
