# 使用ccproxy在本地（192.168.1.9:808）搭建一个http/https代理
# 用户名为root，密码为123456

from urllib.request import ProxyHandler, build_opener
from urllib.error import URLError

username = "root"
password = "123456"
proxy = "{}:{}@192.168.1.9:808".format(username, password)
proxy_handle = ProxyHandler(
    {
        'http': 'http://'+proxy,
        'https': 'https://'+proxy
    }
)

opener = build_opener(proxy_handle)
try:
    response = opener.open("https://httpbin.org/get")
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
