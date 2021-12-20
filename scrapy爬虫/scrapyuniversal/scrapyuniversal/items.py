# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import TakeFirst, Join, Compose
from scrapy.loader import ItemLoader
from scrapy import Field, Item


class YgItem(Item):
    title = Field()
    text = Field()
    image = Field()
    status = Field()
    time = Field()
    id_code = Field()


class Newsloador(ItemLoader):
    default_output_processor = TakeFirst()


class YangguangLoador(Newsloador):
    text_out = Compose(Join(), lambda s: s.strip())
    status_out = Compose(Join(), lambda s: s.strip())
