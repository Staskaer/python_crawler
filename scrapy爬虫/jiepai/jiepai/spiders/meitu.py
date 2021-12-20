import scrapy


class MeituSpider(scrapy.Spider):
    name = 'meitu'
    allowed_domains = ['toutiao.com']
    start_urls = ['https://so.toutiao.com/search?keyword=%E8%A1%97%E6%8B%8D&pd=atlas&dvpf=pc&aid=4916&page_num=1&search_json=%7B%22from_search_id%22%3A%2220210729211604010212194025049F0AC7%22%2C%22origin_keyword%22%3A%22%E8%A1%97%E6%8B%8D%22%2C%22image_keyword%22%3A%22%E8%A1%97%E6%8B%8D%22%7D&rawJSON=1&search_id=202107292121300101501370353FF334B4']
    page = 1
    params = {
        'keyword': '街拍',
        'pd': 'atlas',
        'dvpf': 'pc',
        'aid': '4916',
        'page_num': "",  # 这是需要输入调整的Ajax请求的页面位置
        'search_json': '{"from_search_id":"20210729211604010212194025049F0AC7","origin_keyword":"街拍","image_keyword":"街拍"}', 'rawJSON': '1', 'search_id': '202107292121300101501370353FF334B4'
    }

    def parse(self, response):
        pass
