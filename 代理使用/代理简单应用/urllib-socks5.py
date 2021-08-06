# 使用v2ray在本机（127.0.0.1：1080）搭建一个socks5代理
# 无用户名和密码

import socks
import socket
from urllib import request
from urllib.error import URLError

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)  # 这种方法是全局设置
socket.socket = socks.socksocket
try:
    response = request.urlopen("https://httpbin.org/get")
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
