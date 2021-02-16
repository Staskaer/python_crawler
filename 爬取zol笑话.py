import requests
from bs4 import BeautifulSoup
err = 0


def GetHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def HTMLparseer(html, lst):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('h1', 'article-title').get_text()
        info = soup.find(
            'div', 'article-text').get_text().split('                        ')[1]
        lst.update({name: info})
    except:
        global err
        print("one page missing")
        err += 1


def HTMLwrite(lst, path):
    with open(path, 'a', encoding='utf-8')as f:
        for key, value in lst.items():
            f.write(key)
            f.write('\n')
            f.write(str(value))
            f.write('\n\n')


def main():
    global err
    url = "http://xiaohua.zol.com.cn/detail1/"
    path = r"D:\python_files\zol.txt"
    pages = 100
    conList = {}
    for i in range(1, pages):
        urlevery = url + str(i) + '.html'
        html = GetHTMLText(urlevery)
        HTMLparseer(html, conList)
    HTMLwrite(conList, path)
    print(str(err)+" pages missing\n"+str(pages)+" in total")


main()
