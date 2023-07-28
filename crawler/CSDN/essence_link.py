from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import queue
import asyncio

# 将滚动条向下滚动的java script
js='window.scrollTo(0, document.body.scrollHeight)'

options = EdgeOptions()
options.use_chromium = True
options.binary_location = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # 浏览器的位置
driver = Edge( executable_path="C:\Program Files (x86)\Microsoft Web Driver\msedgedriver.exe") # 相应的浏览器的驱动位置
driver.implicitly_wait(1)
url="https://ask.csdn.net/channel/1005?rewardType&stateType=0&sortBy=1&quick=6&essenceType=1&tagName=essence"

driver.get(url)

# 在两个协程间通讯
channel=queue.Queue()

async def load_page():

    '''
        协程函数，
        负责driver相关操作
        （Selenium WebDriver 不是线程安全的，并且不能在多个协程中共享同一个 WebDriver 实例）
        负责获得当前页面快照传入channel
        然后下滑加载页面
    '''

    # 获得当前页面快照，传入channel
    snapshot=driver.page_source
    global channel
    channel.put(snapshot)
    print("enqueue!")
    # 下滑加载页面
    driver.execute_script(js)
    # 确保加载完毕
    sleep(2)


length=0
links=set()
flag=False
async def parse_page():

    '''
        协程函数，
        负责解析页面快照，
        读取新加载出的链接地址，
        加入set
        同时写入文件备份
    '''
    global length
    print(length)
    global channel
    if channel.empty():
        return
    raw_page=channel.get()
    tree=etree.HTML(raw_page)
    link_list=tree.xpath("/html/body/div[2]/div/main/div/div/div[2]/div[2]/div//a/@href")
    if length==len(link_list):
        global flag
        flag=False
        return
    flag=True
    for ind in range(length,len(link_list)):
        if(link_list[ind].find('https://ask.csdn.net/questions/')!=-1):
            global links
            links.add(link_list[ind])
            # with open("more.txt","a",encoding='utf-8') as file:
            #     file.write(link_list[ind]+'\n')
    # 更新已经读取的链接数目
    length=len(link_list)
    # print("length:",length)
    print("set:",len(links))


async def main():
    
    '''
        主函数
        循环执行两个协程，直至获得目标数目的数据
    '''
    while(True):
        task_list=[]
        task1 = asyncio.create_task(load_page())      
        task_list.append(task1)
        task2 = asyncio.create_task(parse_page())      
        task_list.append(task2)

        await asyncio.gather(*task_list)
        global links
        if(len(links)>3000 or flag==False and len(links)>2800):
            driver.quit()
            for ele in links:
                with open("links_simp.txt","a",encoding='utf-8') as file:
                    file.write(ele+'\n')
            break


asyncio.run(main())