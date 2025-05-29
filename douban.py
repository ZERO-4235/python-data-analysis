import requests
from lxml import etree
import time
import random
import re
import csv
#填写你自己的User-Agent和referer
headers = {
    'User-Agent': '',
    'referer': ''
}
#爬取网页主要内容的函数
def get_data(url, writer):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    movies = html.xpath('//ol[@class="grid_view"]/li')

    for movie in movies:
        title = movie.xpath('.//div[@class="hd"]/a/span[1]/text()')[0]
        score = movie.xpath('.//span[@class="rating_num"]/text()')[0]
        detail_texts = movie.xpath('.//div[@class="bd"]/p[1]/text()')
        director = extract_chinese_director(detail_texts)
        writer.writerow([title, score, director])
        print(f"电影名：{title}，评分：{score}，导演：{director}")

    time.sleep(random.uniform(1, 2))
#定义一个函数来提取导演的中文名
def extract_chinese_director(detail_texts):
    text = ''.join(detail_texts).strip().replace('\n', '').replace('\xa0', '').replace('&nbsp;', '')
    match = re.search(r'导演:\s*([^主]+)', text)
    if match:
        director_info = match.group(1)
        chinese_names = re.findall(r'[\u4e00-\u9fa5·]+', director_info)
        return chinese_names[0] if chinese_names else "未知"  # ✅ 只取第一个
    else:
        return "未知"


if __name__ == '__main__':
    #将代码写入csv表格
    with open('douban_top250.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['电影名', '评分', '导演'])  # 表头只写一次
        #实现翻页
        for i in range(10):  # 共10页，每页25条
            url = f"https://movie.douban.com/top250?start={i*25}"
            get_data(url, writer)



#词云图制作
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('douban_top250.csv')

# 合并导演列，生成词云文本
text = ' '.join(df['导演'].dropna().astype(str))
# 替换掉中间点防止被词云切断
text = text.replace("·", "")  # 或者 text.replace("·", "．")
# 设置中文字体路径（Windows 下常用路径）
font_path = 'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑字体

# 创建词云对象
wc = WordCloud(
    font_path=font_path,  # 关键：指定支持中文的字体
    background_color='white',
    width=800,
    height=600,
    max_words=100
)

# 生成词云
wc.generate(text)

# 显示词云图
plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("豆瓣Top250导演词云", fontsize=400, fontproperties=plt.matplotlib.font_manager.FontProperties(fname=font_path))
plt.show()