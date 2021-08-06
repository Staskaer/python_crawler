# 启动文件
# 此文件用于启动整个代理池

from dispatch import Schedule

if __name__ == '__main__':
    strat = Schedule()
    strat.run()
