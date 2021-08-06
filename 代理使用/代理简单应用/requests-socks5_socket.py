# 使用v2ray在本机（127.0.0.1：1080）搭建一个socks5代理
# 无用户名和密码
# 此处使用全局代理

import socks
import socket
import requests

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)  # 这种方法是全局设置
socket.socket = socks.socksocket
try:
    response = requests.get("https://httpbin.org/get")
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print(e.args)
