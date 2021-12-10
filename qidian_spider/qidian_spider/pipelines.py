# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from elasticsearch import Elasticsearch
from itemadapter import ItemAdapter
from .items import QidianInfoSpiderItem, QidianTypeSpiderItem, QidianBookMsgSpiderItem, QidianBookChapterMsgSpiderItem


class QidianSpiderPipeline:

    def process_item(self, item, spider):
        es = Elasticsearch()
        try:
            if isinstance(item, QidianInfoSpiderItem):
                es.index(index="小说类型", document=ItemAdapter(item).asdict(), id=item["info_type_text"])
        except Exception as error:
            print("......................................" + str(error))
        return item


class QidianTypeSpiderPipeline:
    def process_item(self, item, spider):
        es = Elasticsearch()
        try:
            if isinstance(item, QidianTypeSpiderItem):
                es.index(index=item["info_type_text"], document=ItemAdapter(item).asdict(), id=item["type_title"])
        except Exception as error:
            print("0000000000000000000000000000000000000000000" + str(error))
        return item


class QidianBookMsgSpiderPipeline:
    def process_item(self, item, spider):
        es = Elasticsearch()
        try:
            if isinstance(item, QidianBookMsgSpiderItem):
                es.index(index=item["type_title"], document=ItemAdapter(item).asdict(), id=item["book_name"])
        except Exception as error:
            print("111111111111111111111111111111111111111111111" + str(error))
        return item


class QidianBookMsgSpiderPipeline:
    def process_item(self, item, spider):
        es = Elasticsearch()
        try:
            if isinstance(item, QidianBookChapterMsgSpiderItem):
                es.index(index=item["book_name"], document=ItemAdapter(item).asdict(), id=item["chapters_name"])
        except Exception as error:
            print("111111111111111111111111111111111111111111111" + str(error))
        return item
