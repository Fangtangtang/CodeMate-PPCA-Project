# get introduction 
import requests
import json
import jsonlines
from lxml import etree
catalog = [
           "线性表",
           "堆栈",
           "队列",
           "树_(数据结构)",
           "優先佇列",
           "集合_(计算机科学)",
           "查找表",
           "平衡树",
           "哈希表",
           "排序算法",
           "并查集",
           "图_(数据结构)",
           "最小生成树",
           "最短路问题",
           "算法"
           ]
# 整个网页
header={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
}
url="https://zh.m.wikipedia.org/wiki/{}"
question="{}是什么"

def Get_information(point):
    responese=requests.get(url=url.format(point),headers=header)
    tree=etree.HTML(responese.text)# 解析字符串格式的HTML文档对象，将传进去的字符串转变成Element对象（文档中的元素结点）
                                   # 返回值是一个 Element 对象，表示 HTML 文档的根元素
    introduction=tree.xpath('/html/body/div[1]/div/main/div[3]/div/div[1]/section[1]/p//text()')
    intro=""
    for ele in introduction:
        intro=intro+ele
    dict={"Answer":intro,"Knowledge_Point":"{}".format(point),"Question":question.format(point),"Tag":"数据结构"}
    with jsonlines.open('1.jsonl', 'a') as writer:
        writer.write(dict)

for point in catalog:
    try:
        print(point)
        Get_information(point)
    except BaseException:
        with open ("error","a",encoding="utf-8") as f:
             f.write(point+'\n')
        print("error {}".format(point))
    

