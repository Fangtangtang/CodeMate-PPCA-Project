# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import jsonlines

class CsdnspiderPipeline():
    def process_item(self, item, spider):
        dict={"Answer":item["answer"],"Knowledge_Point":item["point"],"Question":item["question"],"Tag":"数据结构"}
        with jsonlines.open("csdn_extra.jsonl","a") as file:
            file.write(dict)
        return item
