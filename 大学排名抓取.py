import bs4
import requests
from bs4 import BeautifulSoup


def getHTMLText(url):  # 获取HTML页面
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return " "


def fillUnivList(ulist, html):  # 解析HTML页面来获取排名信息
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')  # 等价于tds = tr.find_all('td')
            ulist.append([tds[0].get_text("", strip=True),
                          tds[1].a.string, tds[4].get_text("", strip=True)])    # 存放数据
            # (不知道为啥此处格式化数据成了这个鬼样，血压上升)
            # nmd


def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:<10}"  # 设置输出格式，对齐
    # chr（12288）使用中文空格来填充，以免对齐不准确
    print(tplt.format("排名", "学校名称", "总分", chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))


def main():
    uinfo = []
    url = "https://www.shanghairanking.cn/rankings/bcur/2020"
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20)  # 78 universities


main()
