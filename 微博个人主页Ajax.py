import requests
from urllib.parse import urlencode
from lxml import etree
from redis import StrictRedis
base_url = "https://m.weibo.cn/api/container/getIndex?"
headers = {
    'Referer': "https://m.weibo.cn/u/2830678474",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.json()
    except requests.ConnectionError as e:
        print('ERROR', e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = str(item.get('id'))
            weibo['text'] = str(etree.HTML(item.get('text')).xpath("//text()"))
            weibo['attitudes'] = str(item.get('attitudes_count'))
            weibo['comments'] = str(item.get('comments_count'))
            yield weibo


if __name__ == '__main__':
    text_count = 1
    try:
        redis = StrictRedis(password='123456')
        for i in range(1, 11):
            json_data = get_page(i)
            results = parse_page(json_data)
            for result in results:
                redis.set("text{}".format(text_count),
                          "\n".join(result.values()))
                text_count += 1
    except:
        pass
