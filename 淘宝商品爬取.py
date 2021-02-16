import requests
import re


def getHTMLText(url):  # 常用的那个获取HTML页面的函数
    try:
        headers = {
            'authority': 's.taobao.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 't=42fbaf187ec48b49db8791d9773a4e18; cna=iXmiGHkpnzQCAXnnLAkCaW0g; sgcookie=E100H7x1rrlFuiFnacc0a133EJocgfOo9lA9YdGUH3xsgR8pgxeBsNId5Pyay9R7H5EwIxzNaBoq4Fqo4Y9Xg%2Feh1A%3D%3D; uc3=nk2=F6k3HSxrlW1or2bRfofG%2FZP09XI%3D&vt3=F8dCuAc%2FKVb2jOJrXzs%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&id2=UNN66cIhnuV56g%3D%3D; lgc=t_1506760774136_0988; uc4=nk4=0%40FbMocxnMt51ySC7DJpjYDl%2BCl9OGHIPd9191AD9RLw%3D%3D&id4=0%40UgQyfnefX6w69%2FQX%2BisK0MAnG6al; tracknick=t_1506760774136_0988; _cc_=W5iHLLyFfA%3D%3D; enc=zrFwG9HyKkMOY192abm59B1wcZX5FYc2L1xQqR3QCDQjoPelkfKkMgaG3cAz2ganQjfQd3wu2Cu6%2Fw7O6NNmnw%3D%3D; mt=ci=11_1; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=4fc93e1a2adbc7cff748b7915b2a90f8_1613206700202; _m_h5_tk_enc=2210d08452e5b4990b818a22c7e59470; cookie2=1d905c4831a00fb36b11cab012830caf; _tb_token_=e535636387eeb; xlly_s=1; _uab_collina=161319878888155079711641; x5sec=7b227365617263686170703b32223a223439643530346435343362333230363430653062626565646236663064373562434d54726e594547454d4850706f7564674e2f504f786f4d4d7a4d334f5451304e7a51774f4473784d4b6546677037382f2f2f2f2f77453d227d; uc1=cookie14=Uoe1gWZVFio0vQ%3D%3D; JSESSIONID=E6E9CA348A86E3C37FE8399F46354463; tfstk=c8XAB7xQUz4mWutRYsFo55YK9yWOZfi9SDLtBkceaYMIIIHOiFBhp6XL9huveuC..; l=eBIyRUd7jx6gVlQQBOfalurza779HIRbjuPzaNbMiOCPOu165y5fW6iuhX8BCnGVHsZkR3yEBP-7B7TF0ydZGhZfP3k_J_2IndC..; isg=BCwsf8gEYNj0-nThEA5YAqi2_Qpe5dCP8c-9gYZtTVd6kc2brvQaH2YrsVkpIgjn',
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
