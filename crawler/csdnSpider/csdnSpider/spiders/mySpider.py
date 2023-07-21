import scrapy
from scrapy import Request
from ..items import CsdnspiderItem

import json

URL="https://so.csdn.net/api/v3/search?q={}&t=ask&p={}&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=1&prs=&pre=&ecc=-1&ebc=-1&ia=1&dId=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_code="

catalog=["线性表",
         "栈",
         "队列",
         "树",
         "优先级队列",
         "集合",
         "静态查找表",
         "查找树",
         "散列表",
         "排序",
         "不相交集",
         "图",
         "最小生成树",
         "最短路径",
         "算法设计"
]


class MyspiderSpider(scrapy.Spider):
    cnt=0
    name = "mySpider"
    allowed_domains = ["csdn.net"]

    global URL
    global catalog
    start_urls = [URL.format(catalog[0],i) for i in range(10)]

    def parse(self, response):
        dic=response.json()
        QA_list=dic["result_vos"]       
        for QA in QA_list:
            detail_url=QA["url"]
            item=CsdnspiderItem()
            item['answer']=QA["answer"]
            point = response.meta.get('point')
            # print(1)
            if point is not None:
                item['point']=point
            else:
                item['point']=catalog[0]
            yield Request(url=detail_url, meta={'item': item},callback=self.parse_detail)

        if self.cnt < (len(catalog)-1):
            self.cnt+=1
            # print(catalog,len(catalog))
            # print(self.cnt)
            urls=[URL.format(catalog[self.cnt],i) for i in range(20)]
            for url in urls:
                yield Request(url=url, meta={'point': catalog[self.cnt]})

    def parse_detail(self, response):
        item=response.meta['item']
        title=response.xpath('//section[@class="title-box"]/h1/text()').get()
        ques=response.xpath('//section[@class="question_show_box"]//div[@class="md_content_show"]//text()').get() # 取其中的文本部分
        # print(title)
        item["question"]=title+ques
        yield item
