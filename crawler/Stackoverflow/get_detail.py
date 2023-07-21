import jsonlines
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import threading
import queue
from lxml import etree
import re

URL='https://stackoverflow.com{}'
url_queue=queue.Queue()
semaphore = threading.Semaphore(14)

options = EdgeOptions()
options.use_chromium = True
options.binary_location = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # 浏览器的位置
options.accept_insecure_certs = True
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")



def list2str(list_):
    s=""
    for ele in list_:
        s+=ele
    return s

def tags2str(tags_):
    s=""
    for tag in tags_:
        s+=(tag+',')
    return s

def ProcessUrl(url):
    if semaphore.acquire():
        try:
            driver = Edge( executable_path="C:\Program Files (x86)\Microsoft Web Driver\msedgedriver.exe",options=options) # 相应的浏览器的驱动位置
            driver.implicitly_wait(0.2)
            print('create driver')
            driver.get(url)
            print('get')
            snapshot=driver.page_source
            snapshot=re.sub(r'<code(.*?)>', '<code>```',snapshot)
            snapshot = snapshot.replace('</code>', '```</code>')
            tree=etree.HTML(snapshot)

            title_=tree.xpath("//body/div[3]/div[2]/div/div[1]/div[1]/h1/a//text()")
            title=list2str(title_)
            ques_=tree.xpath('//body/div[3]/div[2]/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/*[not(self::div)]//text()')
            ques=list2str(ques_)

            tags_=tree.xpath('//body/div[3]/div[2]/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div/ul/li//text()')
            tag=tags2str(tags_)
                                        
            tmp=tree.xpath('/html/body//div[@id="answers"]//div[@class="post-layout"]')[0]
            ans_=tmp.xpath('./div[2]/div[@itemprop="text"]//text()')
            ans=list2str(ans_)

            dict={"Answer":(ans),"Knowledge_Point":(tag),"Question":(title+ques),"Tag":"data-structures"}
            with jsonlines.open("3.jsonl","a") as file:
                file.write(dict)
                
            driver.quit()

        except BaseException:
            driver.quit()
            with open ("error","a",encoding="utf-8") as f:
                f.write(url+'\n')
            print("error {}".format(url))

        semaphore.release()



file=open("data/link3","r",encoding='utf-8')
lines=file.readlines()
for line in lines:
    url_=line.replace('\n','')
    url_queue.put(url_)


while(not url_queue.empty()):
    url=url_queue.get()
    task = threading.Thread(target=ProcessUrl,args=(URL.format(url),))
    task.start()
