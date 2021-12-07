# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from elasticsearch import Elasticsearch
from itemadapter import ItemAdapter


class QidianSpiderPipeline:

    def process_item(self, item, spider):
        es = Elasticsearch()
        es.index("小说类型", document=ItemAdapter(item).asdict())
        return item
