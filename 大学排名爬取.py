import requests
from bs4 import BeautifulSoup
import re
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url , timeout = 30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return " "

def fillUnivList(ulist,html):
    soup = BeautifulSoup(html,'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr , bs4.element.Tag):
            tds = tr('td')    ##等价于tds = tr.find_all('td')
            ulist.append([tds[0].get_text("",strip=True),tds[1].a.string,tds[4].get_text("",strip=True)])   ###存放数据

def printUnivList(ulist,num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:<10}"   ###设置输出格式，对齐
    print(tplt.format("排名","学校名称","总分", chr(12288)))   
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0],u[1],u[2],chr(12288)))


def main():
    uinfo = []
    url = "https://www.shanghairanking.cn/rankings/bcur/2020"
    html = getHTMLText(url)
    fillUnivList(uinfo,html)
    printUnivList(uinfo,20)   ### 78 universities

main()
