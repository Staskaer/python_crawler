import requests
import re
from bs4 import BeautifulSoup
import traceback


def getHTMLText(url):  # 获得页面信息
    try:
        kv = {"user-agent": "Mozilla/5.0"}  # 设置headers
        r = requests.get(url, headers=kv, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return "getHTMLText error"


def getStockList(lst, StockURL):  # 解析html页面获得股票代码，存到list中
    html = getHTMLText(StockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')  # 找到所有a标签
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r"[S][HZ]\d{6}", href)[0])
        except:
            continue  # 如果遇到不符合字符串就直接略过，保证全部找到


def getStockInfo(lst, StockURL, fpath):  # 将获得的列表中的股票一一爬取下来
    infoDict = {}
    for stock in lst:
        url = StockURL + stock
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, "html.parser")
            StockInfo = soup.find('div', 'stock-current').string  # 存储股票价格
            StockName = soup.find('div', 'stock-name').string.split('(')[0]  # 存储股票名称
            infoDict.update({StockName: StockInfo})  # 将爬取的股票名称，价格以键值对的方式存入字典

        except:
            traceback.print_exc()
            continue
    with open(fpath, 'a', encoding='utf-8')as f:  # 保存到文件中
        for key, value in infoDict.items():
            f.write(key)
            f.write('\t:\t')
            f.write(str(value))
            f.write('\n')


def main():
    Stock_list_URL = "https://hq.gucheng.com/dapangu.html?sort_field_name=px_change_rate&sort_type=desc&page="
    Stock_info_URL = "https://xueqiu.com/S/"
    output_file = r"D:\python_files\股票爬取结果.txt"
    slist = []
    for i in range(1, 2):  # 绝对绝对绝对不能过大（会把自己的内存爬爆掉）（P.S.优化拉跨)
        url = Stock_list_URL + str(i)
        getStockList(slist, url)
    getStockInfo(slist, Stock_info_URL, output_file)


main()
