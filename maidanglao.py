

#   使用selenium来爬取麦当劳的所有菜品
#下列一大串大代码都是配置环境
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
import time

options = Options()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#定义一个主函数
def get_data_mdl(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(0.5)
    data = driver.page_source
    html = etree.HTML(data)
    title = html.xpath('//span[@class="name"]/text()')
    print(title)
    driver.quit()
if __name__ == '__main__':
    #网页每一个后缀都不同，需要使用循环来翻页
    list_1 = {"hamburgers", "beverage", "Snacks", "desserts", "Breakfast-26", "Happy-Meal-Items-2"}
    for item in list_1:
        url = f"https://www.mcdonalds.com.cn/product/mcdonalds/{item}"
        get_data_mdl(url)
