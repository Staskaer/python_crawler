# 调度模块，负责检测模块，接口模块和爬取模块的调度策略
# 暂时还未编写接口模块
from testproxy import Tester
from testproxy import Test_max_score
from getter import Getter
from multiprocessing import Process
from time import sleep

from settings import TEST_CYCLE
from settings import GETTER_CYCLE
from settings import TEST_ENABLE
from settings import GETTER_ENABLE
from settings import API_ENABLE
from settings import API_HOST
from settings import API_PORT
from settings import MAX_SCORE_ENABLE
from settings import MAX_SCORE_CYCLE
from api import app


class Schedule(object):
    def schedule_tester(self, cycle=TEST_CYCLE):
        tester = Tester()
        while True:
            try:
                print("测试器开始运行...")
                tester.run()
                sleep(cycle)
            except:
                print("测试器出错中止，3秒后重新启动...")
                sleep(3)

    def max_score_test(self, cycle=MAX_SCORE_CYCLE):
        tester = Test_max_score()
        while True:
            try:
                print("开始测试满分代理...")
                tester.run()
                sleep(cycle)
            except:
                print("满分测试器出错中止，3秒后重新启动...")
                sleep(3)

    def schedule_getter(slef, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            try:
                print("开始抓取代理...")
                getter.run()
                sleep(cycle)
            except:
                print("代理爬取过程出错，3秒后重新启动...")
                sleep(3)

    def schedule_api(self):
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        print("代理池开始运行")
        if TEST_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()

        if MAX_SCORE_ENABLE:
            max_score_process = Process(target=self.max_score_test)
            max_score_process.start()


if __name__ == '__main__':
    a = Schedule()
    a.run()
