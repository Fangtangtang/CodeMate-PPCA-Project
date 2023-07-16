import requests
from lxml import etree
import jsonlines

header = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
    'Host':'so.csdn.net'
}

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
         "图","最小生成树",
         "最短路径",
         "算法设计"
]

def get_all_QAs(main_url,page,point):
    url=main_url
    print("page{}!".format(page))
    
    response=requests.get(url=url,headers=header)
    dic=response.json()
    QA_list=dic["result_vos"]
    for QA in QA_list:
        detail_url=QA["url"]
        response=requests.get(detail_url)
        tree=etree.HTML(response.text)
        if(tree==None): return
        title=tree.xpath('//section[@class="title-box"]/h1/text()')
        ques=tree.xpath('//section[@class="question_show_box"]//div[@class="md_content_show"]//text()') # 取其中的文本部分
        question=title+ques
        answer=QA["answer"]
        dict={"Answer":answer,"Knowledge_Point":"{}".format(point),"Question":question,"Tag":"数据结构"}
        with jsonlines.open("csdn_extra.jsonl","a") as file:
            file.write(dict)

# 1-20      
url="https://so.csdn.net/api/v3/search?q={}&t=ask&p={}&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=1&prs=&pre=&ecc=-1&ebc=-1&ia=1&dId=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_code="
for point in catalog:   
    for i in range(1,20):
        point_url=url.format(point,i)
        try:
            get_all_QAs(point_url,i,point)
        except BaseException:
            with open ("error","a",encoding="utf-8") as f:
                f.write(point+"{}".format(i)+'\n')
            print("error {} {}".format(point,i))