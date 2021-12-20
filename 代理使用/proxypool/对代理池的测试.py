# 此文件用于测试代理池的性能（与代理池本身无关）
# 测试的是经过代理筛选过后通过api提取出的代理的可用性
# 抓取到的代理均为支持https的代理，但是有部分代理非高匿代理

import requests
import re


HTTP_API = '127.0.0.1:5555'


def get_via_proxy():
    gaoni = 0
    putong = 0
    failed = 0
    count = 0
    while True:
        count += 1
        proxy_via_api = requests.get("http://127.0.0.1:5555/random")
        print("代理为:", proxy_via_api.text)
        proxy = {
            'http': 'http://'+proxy_via_api.text,
            'https': 'https://'+proxy_via_api.text
        }
        try:
            r = requests.get("https://httpbin.org/get",
                             proxies=proxy, timeout=10)
            orign = re.findall(r"(?:\d+\.){3}\d+", r.text)
            if len(orign) == 1:
                gaoni += 1
                print("高匿代理")
            else:
                putong += 1
                print("普通代理")
            print("请求源", orign)
        except:
            failed += 1
            print("失败")
        if count % 10 == 0:
            print("=====测试报告====")
            print("\n总计 = {},普通代理 = {},高匿代理 = {},失败 = {}\n".format(
                count, putong, gaoni, failed))
            print("================")


get_via_proxy()

# 结论：
# 代理可用率约为40%
# 由于redis中代理过多，测试进程每次测试能力有限
# 所以会有部分失效代理仍未满分留在redis的api中
# 导致代理池出现明显的不稳定周期
# 所以考虑增加一个辅助检测模块，这个模块仅对满分代理进行短周期检查
# 以确保在api调用范围的代理被高频率检测减少故障率

# 21.8.6已添加上述实现
# 代理可用率约为60%
# 但性能未显著提升
# 原因：免费代理时效性太短，导致代理变化迅速
# 策略：缩短满分测试代理的超时时间

# 已实现
# 一次测试结果可用率接近80%

# 经验证，发现部分代理为普通代理，用处不大，应该永久性的在代理池中ban掉普通代理
