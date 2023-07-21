import jsonlines
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from lxml import etree

options = EdgeOptions()
options.use_chromium = True
options.binary_location = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # 浏览器的位置
opt = EdgeOptions()
opt.accept_insecure_certs = True

url='https://stackoverflow.com/questions/tagged/data-structures?tab=votes&page={}&pagesize=50'

for i in range(300,450):
    try: 
        driver = Edge( executable_path="C:\Program Files (x86)\Microsoft Web Driver\msedgedriver.exe",options=opt) # 相应的浏览器的驱动位置
        driver.implicitly_wait(0.5)
        btn_list=driver.find_elements_by_class_name("flex--item6 s-btn s-btn__primary js-reject-cookies js-consent-banner-hide")
        print(len(btn_list))
        detail_url=url.format(i)                               
        driver.get(detail_url)
        time.sleep(1)
        snapshot=driver.page_source
        tree=etree.HTML(snapshot)
        link_list=tree.xpath("/html/body/div[3]/div[2]/div[1]/div[5]/div/div[2]/h3/a/@href")
        for link in link_list:
            with open("links","a",encoding='utf-8') as file:
                file.write(link+'\n')

        driver.quit()
    except BaseException:
        with open ("error","a",encoding="utf-8") as f:
            f.write("{}".format(i)+'\n')
        print("error {}".format(i))

                        
