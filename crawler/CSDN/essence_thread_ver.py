import jsonlines
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
import queue
import threading
import re
from lxml import etree 

semaphore = threading.Semaphore(14)

options = EdgeOptions()
options.use_chromium = True
options.binary_location = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # 浏览器的位置


def ProcessUrl(url):
    if semaphore.acquire():
        try:
            driver = Edge( executable_path="C:\Program Files (x86)\Microsoft Web Driver\msedgedriver.exe",options=options) # 相应的浏览器的驱动位置
            driver.implicitly_wait(0.1)
            driver.get(url=url)
            # 找到页面中所有的“展开全部”按钮，单击展开
            # （否则无法通过driver读取完整）
            btn_list=driver.find_elements_by_class_name("expandBtn")
            act_chains=ActionChains(driver)
            for btn in btn_list:
                act_chains.click(btn)
            act_chains.perform()

            snapshot=driver.page_source
            # 将代码块用```包裹
            snapshot=re.sub(r'<code(.*?)>', '<code>```',snapshot)
            snapshot = snapshot.replace('</code>', '```</code>')
            tree=etree.HTML(snapshot)

            title_=tree.xpath('//main/div/div[1]/div[1]/section[3]/h1//text()')
            ques_=tree.xpath('//main/div/div[1]/div[1]/section/div/div[1]/div/div/div/div//text()')
            question=''
            for ele in title_:
                 question+=ele
            for ele in ques_:
                 question+=ele
            answer_=tree.xpath('/html/body/div/div/main/div/div[1]/div[2]/div/div/div[1]/ul[1]/li/div[1]/div/div/div/div/div//text()')
            answer=''
            for ele in answer_:
                 answer+=ele
            point_=tree.xpath('/html/body/div[3]/div/main/div/div[1]/div[1]/section[4]/div/div/ul/li/a//text()')
            point=''
            for ele in point_:
                 point+=(ele+',')
            diction={"Answer":answer,"Knowledge_Point":point,"Question":question,"Tag":"数据结构与算法"}
            with jsonlines.open("essence.jsonl","a") as file:
                file.write(diction)

        except BaseException:
            with open ("error","a",encoding="utf-8") as f:
                f.write(url+'\n')
            print("error {}".format(url))

        driver.quit()
        semaphore.release()

# 构建所有链接的队列
link_list=queue.Queue()
file=open("copy","r",encoding='utf-8')
lines=file.readlines()
for line in lines:
    link=line.replace('\n','')
    link_list.put(link)

print("gotten link!")

while not link_list.empty():
        url=link_list.get()
        task=threading.Thread(target=ProcessUrl,args=(url,))
        task.start()

