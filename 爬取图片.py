import requests
import os

url = "https://www.assdrty.com/images/2021/01/12/6B0qn5B.jpg"
root = "D:/python_files/abc.jpg"
kv = {'user-agent' : 'Mozilla/5.0'}

r = requests.get(url,headers = kv)

with open(root,'wb') as f:
    f.write(r.content)
