# 定义了继承requests对象的WeixnRequests类

from requests import Request

from settings import TIMEOUT


class WinxinRequests(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method=method, url=url, headers=headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout
