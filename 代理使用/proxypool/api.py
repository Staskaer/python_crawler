# 接口模块，用于输出代理

from flask import Flask, g
from save_ import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welecome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(host='192.168.1.9', port=5555)
