FROM python:3.9.6

MAINTAINER Coolin

ADD . /scrapy_crawl/dd

WORKDIR /scrapy_crawl/dd

RUN pip install -r requirement.txt

CMD scrapy crawl 'book'