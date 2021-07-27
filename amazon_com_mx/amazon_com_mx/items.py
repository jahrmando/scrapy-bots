# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from datetime import datetime
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags, strip_html5_whitespace, replace_entities


def clean_number(value):
    return re.sub(r'[$,#]', '', value)

def clean_stars(value):
    return re.search(r'\d.?\d', value).group(0)  

def get_url_value(value):
    match = re.search(r'.*(sellers|dp)\/(\w+)(\/|\?).+', value)
    return match.group(2) if match else value


class Product(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, clean_number),
        output_processor=TakeFirst(),
    )
    rank = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, clean_number),
        output_processor=TakeFirst(),
    )
    reviews = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, clean_number),
        output_processor=TakeFirst(),
    )
    stars = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, clean_stars),
        output_processor=TakeFirst(),
    )
    asin = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, replace_entities, get_url_value),
        output_processor=TakeFirst(),
    )
    category = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, get_url_value),
        output_processor=TakeFirst(),
    )
    sub_category = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=TakeFirst(),
    )
