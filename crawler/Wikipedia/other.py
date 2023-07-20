# manage the ones without catalog
import requests
import jsonlines
from lxml import etree
catalog = [
           "线性表",
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
    dict={"Answer":introduction,"Knowledge_Point":"{}".format(point),"Question":question.format(point),"Tag":"数据结构"}
    with jsonlines.open('wiki.jsonl', 'a') as writer:
        writer.write(dict)
    head1=tree.xpath('/html/body/div[1]/div/main/div[3]/div/div[1]/h2')
    ans1=tree.xpath('/html/body/div[1]/div/main/div[3]/div/div[1]/section')
    length=len(head1)
    for i in range(0,length,1):
        name=head1[i].xpath('./span[2]//text()')[0]
        if(name=="参考文献" or name=="参见" or name=="參見"): break
        if (name.find("{}".format(point))==-1): name=point+"的"+name
        answer=ans1[i+1].xpath('.//text()')
        dict={"Answer":answer,"Knowledge_Point":"{}".format(point),"Question":question.format(name),"Tag":"数据结构"}
        with jsonlines.open('wiki_main.jsonl', 'a') as writer:
            writer.write(dict)

# file=open("copy","r",encoding='utf-8')
# lines=file.readlines()
for point in catalog:
    # point=line.replace('\n','')
    try:
        print(point)
        Get_information(point)
    except BaseException:
        with open ("error","a",encoding="utf-8") as f:
             f.write(point+'\n')
        print("error {}".format(point))
    

