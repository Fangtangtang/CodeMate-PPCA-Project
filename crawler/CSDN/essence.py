import jsonlines
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
import queue
import asyncio

knowledge_points=["线性表",
                "栈",
                "队列",
                "树",
                "集合",
                "查找表",
                "查找树",
                "散列表",
                "排序",
                "不相交集",
                "图",
                "最小生成树",
                "最短路径",
                "递归",
                "算法" 
]

p_dict={'c':['c','C'],
        'c++':['c++','C++'],
        'python':['python','Python','PYTHON'],
        'java':['java','Java','JAVA'],
        'matlab':['MatLab','MATLAB','matlab']
}

def get_knowledge_point(title):
    for point in knowledge_points:
        if(title.find(point)!=-1):
            return point
    for key in p_dict:
        for point in p_dict[key]:
            if(title.find(point)!=-1):
                return point 
    return '数据结构、算法'


options = EdgeOptions()
options.use_chromium = True
options.binary_location = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # 浏览器的位置
# driver = Edge( executable_path="C:\Program Files (x86)\Microsoft Web Driver\msedgedriver.exe") # 相应的浏览器的驱动位置
# driver.implicitly_wait(1)

# 构建所有链接的队列
link_list=queue.Queue()
file=open("links_simp.txt","r",encoding='utf-8')
lines=file.readlines()
for line in lines:
    point=line.replace('\n','')
    link_list.put(point)

print("gotten link!")

async def pipeline(driver):

    '''
        协程函数
        一个driver的工作区
        从队列中取地址，读取信息，构建dict，写入jsonl文件
        直到queue为空
    '''
    while not link_list.empty():
        url=link_list.get()
        print(url)
        driver.get(url=url)
        # 找到页面中所有的“展开全部”按钮，单击展开
        # （否则无法通过driver读取完整）
        btn_list=driver.find_elements_by_class_name("expandBtn")
        act_chains=ActionChains(driver)
        for btn in btn_list:
            act_chains.click(btn)
        act_chains.perform()
        title=driver.find_element_by_xpath('//main/div/div[1]/div[1]/section[3]/h1').text
        ques=driver.find_element_by_xpath('//main/div/div[1]/div[1]/section[5]/div/div[1]/div/div/div/div').text
        question=ques+title
        answer=driver.find_element_by_xpath('/html/body/div[3]/div/main/div/div[1]/div[2]/div/div/div[1]/ul[1]/li/div[1]/div/div/div/div/div').text
        point=get_knowledge_point(title)
        diction={"Answer":answer,"Knowledge_Point":point,"Question":question,"Tag":"数据结构与算法"}
        with jsonlines.open("essence.jsonl","a") as file:
            file.write(diction)
    
async def main():
    '''
        主函数
        构建多个driver
        各个工作区并行
    '''
    num=5
    drivers=[]
    task_list=[]
    for i in range(0,num):
        driver = Edge( executable_path="C:\Program Files (x86)\Microsoft Web Driver\msedgedriver.exe") # 相应的浏览器的驱动位置
        driver.implicitly_wait(0.5)
        drivers.append(driver)
        tast=asyncio.create_task(pipeline(driver=driver))
        task_list.append(tast)

    await asyncio.gather(*task_list)

    for driver in drivers:
        driver.quit()
    
asyncio.run(main())

