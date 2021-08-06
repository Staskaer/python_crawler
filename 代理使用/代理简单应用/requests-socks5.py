# 使用v2ray在本机（127.0.0.1：1080）搭建一个socks5代理
# 无用户名和密码

import requests
proxy = "127.0.0.1:1080"
proxies = {
    'http': 'socks5://'+proxy,
    'https': 'socks5://'+proxy
}
try:
    response = requests.get("https://httpbin.org/get", proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print(e.args)
