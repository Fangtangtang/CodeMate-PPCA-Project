import requests
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
url="https://zh.wikipedia.org/zh-cn/{}"
question="{}是什么"

def get_information(point):
    print(point)
    responese=requests.get(url=url.format(point),headers=header)
    tree=etree.HTML(responese.text)# 解析字符串格式的HTML文档对象，将传进去的字符串转变成Element对象（文档中的元素结点）
                                    # 返回值是一个 Element 对象，表示 HTML 文档的根元素
    path=tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/div/ul//a/@href')
    # 获取词条目录
    path_list=[]
    for p in path:
        if p[0]!='#': continue
        p= p[1:]
        path_list.append(p)
    # print(path_list)
    size=len(path_list)
    if(size==0): 
        with open ("main_other","a",encoding="utf-8") as f:
             f.write(point+'\n')
        print("special {}".format(point))
        return
    h1=point+"的"
    h2=""
    h3=""
    h4=""
    h5=""
    for i in range(0,size-1):
        first_title = path_list[i]
        if(first_title=="参考文献" or first_title=="参见" or first_title=="參見"or first_title=="外部链接"or first_title=="注释"): return
        second_title=path_list[i+1]
        node1=tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]//span[@id="{}"]'.format(first_title))[0]
        node2=tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]//span[@id="{}"]'.format(second_title))[0]
        father1=node1.getparent()
        father2=node2.getparent()
        while(father1!=father2):
            node1=father1
            node2=father2   
            father1=node1.getparent()
            father2=node2.getparent()    
        start=father1.index(node1) # 返回类似列表，用index定位到其中的元素（所有的head同级）
        end=father2.index(node2) # 找到在同一颗树下的一维结点位置（将立体tree向右压扁）

        name=father1[start].xpath('.//span[@class="mw-headline"]//text()')
        if node1.tag=='h2' :
            h2=name[0]
            h3=""
            h4=""
            h5=""
        if node1.tag=='h3' :
            if(len(h2)==0 or h2[-1]!="的"):h2+="的"
            h3=name[0]
            h4=""
            h5=""
        if node1.tag=='h4' :
            if(len(h3)==0 or h3[-1]!="的"): h3+="的"
            h4=name[0]
            h5=""
        if node1.tag=='h5' :
            if(len(h4)==0 or h4[-1]!="的"): h4+="的"
            h5=name[0]   
        text=""
        for i in range(start+1,end):
            element = father1[i]
            # 使用xpath方法找到所有的text节点
            text_nodes = element.xpath('.//text()')
            # 将text节点的内容添加到text字符串
            for text_node in text_nodes:
                text += text_node
        dict={"Answer":text,"Knowledge_Point":"{}".format(point),"Question":question.format(h1+h2+h3+h4+h5),"Tag":"数据结构"}
        with jsonlines.open("wiki_main.jsonl","a") as file:
            file.write(dict)

    # 最后一组特判
    name=father1[end].xpath('.//span[@class="mw-headline"]//text()')
    if(name[0]=="参考文献" or name[0]=="参见" or name[0]=="參見"or name[0]=="外部链接"or name[0]=="注释"): return
    if node1.tag=='h2' :
        h2=name[0]
        h3=""
        h4=""
        h5=""
    if node1.tag=='h3' :
        if(len(h2)==0 or h2[-1]!="的"):h2+="的"
        h3=name[0]
        h4=""
        h5=""
    if node1.tag=='h4' :
        if(len(h3)==0 or h3[-1]!="的"): h3+="的"
        h4=name[0]
        h5=""
    if node1.tag=='h5' :
        if(len(h4)==0 or h4[-1]!="的"): h4+="的"
        h5=name[0]
    text=""
    length=len(father1)
    for i in range(end+1,length):
        element = father1[i]
        # 使用xpath方法找到所有的text节点
        text_nodes = element.xpath('.//text()')
        # 将text节点的内容添加到text字符串
        for text_node in text_nodes:
            text += text_node
    dict={"Answer":text,"Knowledge_Point":"{}".format(point),"Question":question.format(h1+h2+h3+h4+h5),"Tag":"数据结构"}
    with jsonlines.open("wiki_main.jsonl","a") as file:
        file.write(dict)
    
    print("completed {}!".format(point))

# file=open("copy","r",encoding='utf-8')
# lines=file.readlines()
for point in catalog:
    # point=line.replace('\n','')
    
    try:get_information(point)
    except BaseException:
        with open ("error","a",encoding="utf-8") as f:
             f.write(point+'\n')
        print("error {}".format(point))

