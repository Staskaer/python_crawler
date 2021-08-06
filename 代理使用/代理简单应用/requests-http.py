# 使用ccproxy在本地（192.168.1.9:808）搭建一个http/https代理
# 用户名为root，密码为123456

import requests

username = "root"
password = "123456"
proxy = "{}:{}@192.168.1.9:808".format(username, password)
proxies = {
    'http': 'http://'+proxy,
    'https': 'https://'+proxy
}
try:
    response = requests.get("https://httpbin.org/get", proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print(e.args)
