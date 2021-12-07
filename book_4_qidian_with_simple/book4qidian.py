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
                "type_url": parse.urljoin(self.base_url, a_obj.get("href")),
                "type_title": a_obj.get("title")
            }
            all_type_list.append(items)
        return all_type_list


# if __name__ == '__main__':
#     gmb = GetMesg4Book()
#     resp = gmb.get_info_qidian()
#     all_type_list = gmb.paras_qidian_info(resp)
#     print(all_type_list)

from elasticsearch import Elasticsearch

es = Elasticsearch()
# doc = {
#     'title': '历史小说',
#     'text': '历史',
#     'url': 'http://www.qidian.com/lishi/',
#     'count': 5674
# }
# res = es.index(index="小说类型", id='2', document=doc)
# print(res['result'])
# res = es.update(index="小说类型", id='2', doc=doc)
# print(res)

# resp = es.get(index="小说类型", id='2')
# print(resp['_source'])
resp = es.search(
    query={
        "match": {
            "_index": "小说类型"
        }
    }
)
print(resp)
resp = es.search(
    query={
        "match": {
            "info_type_title": "历史"
        }
    }
)
print(resp)

{
    'took': 78,
    'timed_out': False,
    '_shards': {
        'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0
    },
     'hits': {
         'total': {'value': 2, 'relation': 'eq'},
         'max_score': 1.0,
         'hits': [
             {'_index': '小说类型', '_type': '_doc', '_id': '1', '_score': 1.0,
              '_source': {'title': '玄幻小说', 'text': '玄幻', 'url': 'http://www.qidian.com/xuanhuan/', 'count': 1234}
              },
             {'_index': '小说类型', '_type': '_doc', '_id': '2', '_score': 1.0,
              '_source': {'title': '奇幻小说', 'text': '奇幻', 'url': 'http://www.qidian.com/qihuan/', 'count': 567438}
              }
        ]
    }
 }


{
    'took': 1,
    'timed_out': False,
    '_shards': {
        'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0
    },
    'hits': {
        'total': {'value': 2, 'relation': 'eq'},
        'max_score': 1.0,
        'hits': [
            {
                '_index': '小说类型',
                '_type': '_doc',
                '_id': '1',
                '_score': 1.0,
                '_source': {
                    'title': '玄幻小说', 'text': '玄幻', 'url': 'http://www.qidian.com/xuanhuan/', 'count': 1234
                }
            },
            {
                '_index': '小说类型',
                '_type': '_doc',
                '_id': '2',
                '_score': 1.0,
                '_source': {
                    'title': '奇幻小说', 'text': '奇幻', 'url': 'http://www.qidian.com/qihuan/', 'count': 567438
                }
            }
        ]
    }
}


{
    'took': 2,
    'timed_out': False,
    '_shards': {
        'total': 7,
        'successful': 7,
        'skipped': 0,
        'failed': 0
    },
    'hits': {
        'total':
            {
                'value': 1,
                'relation': 'eq'
            },
        'max_score': 4.431637,
        'hits': [
            {
                '_index': '小说类型',
                '_type': '_doc',
                '_id': '0gqDk30BTJsqLxkm9xA8',
                '_score': 4.431637,
                '_source': {
                    'info_type_text': '历史',
                    'info_type_url': 'http://www.qidian.com/lishi/',
                    'info_type_title': '历史小说',
                    'info_type_count': '77225',
                    'spider_name': 'qidian_info',
                    'spider_datetime': '2021-12-07 14:10:39'
                }
            }
        ]
    }
}