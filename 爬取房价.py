import requests
from bs4 import BeautifulSoup
for page in range(1, 5):  # 抓取前5页（每页30条）
    url = f"https://beijing.anjuke.com/sale/p={page*1}"

    headers = {"user-agent":""}
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'  # 确保正确解析中文
    html = response.text

# 解析页面
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='property-content-info')

# 提取数据
    for item in items:
    # 名称
        name_tag = item.find('p', class_='property-content-info-comm-name')
        name = name_tag.text.strip() if name_tag else "未知小区"

    # 价格（根据最新页面结构调整）
        price_tag = item.find('p', class_='property-price-average')
        price = price_tag.text.strip() if price_tag else "价格待询"

    # 地址
        address_tag = item.find('p', class_='property-content-info-comm-address')
        address = address_tag.text.strip() if address_tag else "地址未知"

        print(f"""
                小区：{name}
                价格：{price}
                地址：{address}
                """)
    response.close()