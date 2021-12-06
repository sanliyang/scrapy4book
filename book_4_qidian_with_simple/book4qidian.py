#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time :2021/12/6 15:22
# @Author : liby
# @File: book4qidian.py
# @Software : PyCharm
import requests
from bs4 import BeautifulSoup
from urllib import parse


class GetMesg4Book:
    """
    获取起点小说首页的小说分类信息, 以及不同分类小说的书本个数
    """

    def __init__(self):
        self.base_url = "https://www.qidian.com/"

    def get_info_qidian(self):
        resp = requests.get(self.base_url)
        return resp

    def paras_qidian_info(self, resp):
        bs_obj = BeautifulSoup(markup=resp.content, features="lxml")
        div_obj = bs_obj.find('div', {
            "class": "classify-list fl so-awesome"
        })
        dd_list = div_obj.find_all('dd')
        all_type_list = []
        for dd_obj in dd_list:
            a_obj = dd_obj.a
            items = {
                "type_text": a_obj.i.text,
                "type_url": parse.urljoin(self.base_url,a_obj.get("href")),
                "type_title": a_obj.get("title")
            }
            all_type_list.append(items)
        return all_type_list


if __name__ == '__main__':
    gmb = GetMesg4Book()
    resp = gmb.get_info_qidian()
    all_type_list = gmb.paras_qidian_info(resp)
    print(all_type_list)