import requests
import re


def getHTMLText(url):  # 常用的那个获取HTML页面的函数
    try:
        headers = {
            'authority': 's.taobao.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 ',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': ''
        }   # 这是cookie，由于淘宝反爬，必须要先登录才能获取信息
        # 需要重新获取
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("页面抓取失败")
        return " "


def parsePage(ilt, html):  # 解析HTML页面
    try:
        plt = re.findall(r'\"view_price\":\"[\d\.]*\"', html)  # 使用正则表达式来搜索获取信息
        tlt = re.findall(r'\"raw_title\":\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])  # 将键值对分开，同时去除引号
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print("")


def printGoodList(ilt):  # 输出结果
    tplt = "{:4}\t{:8}\t{:16}"  # 设置输出格式，使页面表现更加美观
    print(tplt.format("序号", "价格", "名称"))
    count = 0
    for g in ilt:
        count = count+1
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = '电脑'  # 搜索商品
    depth = 10  # 搜索页面纵深
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):  # 根据页面选定深度进行搜索爬取
        try:
            url = start_url + '$s=' + str(44*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodList(infoList)


main()
