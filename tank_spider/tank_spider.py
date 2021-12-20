from __future__ import with_statement
import requests
from bs4 import BeautifulSoup
import os
import execjs

#js_compile = execjs.compile(r"D:\vs_code_files\python\projects\爬虫\tank_spider\fun.js")
name = 1
num = 0


def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open(r"D:\vs_code_files\python\projects\爬虫\tank_spider\fun.js",
             'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


jsstr = get_js()
ctx = execjs.compile(jsstr)


def htmlGetText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except:
        return " "


def htmlParser(text):
    try:
        soup = BeautifulSoup(text, parser="html.parser")
        lt = soup.find_all(class_="BDE_Image")
        return lt
    except:
        return []


def imageSave(src_lt):
    global name, num
    root = str(os.getcwd()) + "\image_raw\\"
    isexist = os.path.exists(root.rstrip("\\"))
    if not isexist:
        os.makedirs(root.rstrip("\\"))
    for i in src_lt:
        src = i.attrs["src"]
        try:
            with open(root + str(name)+".jpg", 'xb') as f:
                r = requests.get(src)
                f.write(r.content)
                name += 1
                num += 1
        except FileExistsError:
            name += 1
            num += 1


def transform(root_raw):  # 待完成的转换功能
    global num
    open_name = 1
    root = str(os.getcwd()) + "\image_trans\\"
    isexist = os.path.exists(root.rstrip("\\"))
    if not isexist:
        os.makedirs(root.rstrip("\\"))
    for i in range(num):
        try:
            with open(root_raw + str(open_name)+".jpg", 'b') as f:
                result = ctx.call('ipt2', f)
                print(open_name)
                with open(root+str(open_name)+".jpg", 'xb') as f2:
                    print("start")
                    f2.write(result)
                    print("success")
        except:
            continue


def main():
    start = input("请输入起始页面 : ")
    page = eval(input("请输入爬取页数 : "))
    page = page*2
    pn = 1
    for i in range(page):
        url = start + "?pn=" + str(pn)
        pn += 1
        text = htmlGetText(url)
        src_lt = htmlParser(text)
        imageSave(src_lt)
    print("爬取完成，准备进行转换...")
    transform(str(os.getcwd()) + "\image_raw\\")


main()
