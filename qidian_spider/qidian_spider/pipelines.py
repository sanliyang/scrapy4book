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
        es.index(index="小说类型", document=ItemAdapter(item).asdict(), id=item["info_type_text"])
        return item

class QidianTypeSiderPipeline:
    def process_item(self, item, spider):
        es = Elasticsearch()
        es.index(index=item["info_type_text"], document=ItemAdapter(item).asdict(), id=item["type_title"])
        return item
