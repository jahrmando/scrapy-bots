import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from amazon_com_mx.items import Product


class TopSellersSpider(CrawlSpider):
    name = 'top_sellers'
    allowed_domains = ['amazon.com.mx']
    start_urls = ['https://www.amazon.com.mx/gp/bestsellers/']

    main_categories = set()

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=[
                r'//ul[@id="zg_browseRoot"]/ul/li[2]/a'
            ]),
        ),
        Rule(
            LinkExtractor(restrict_xpaths=[
                r'//*[@id="zg_browseRoot"]/ul/ul/li[*]/a',
                r'//li[@class="a-last"]//a',
            ]), callback='get_products', follow=True
        ),
    )

    
    def parse_main_category(self, response): 
        self.logger.info('Hi, from first rule! %s', response.url)
        self.main_categories.add(response.url)


    def parse_level2_category(self, response):
        self.logger.info('Hi, from second rule! %s', response.url)


    def get_products(self, response):
        self.logger.info('Hi, from third rule! %s', response.url)
        
        sub_category = response.selector.css('span.zg_selected').get()
        products = response.selector.xpath('//li[@class="zg-item-immersion"]')
        
        for product in products:
            load = ItemLoader(Product(), product)

            load.add_xpath('name', './/a/div/text()')
            load.add_xpath('price', ".//span[@class='a-size-base a-color-price']/span/text()")
            load.add_xpath('reviews', './/div/a[2]/text()')
            load.add_xpath('stars', './/div/a/i/span/text()')
            load.add_xpath('asin', './/a/@href')
            load.add_value('category', response.url)
            load.add_value('sub_category', sub_category)
            load.add_xpath('rank', ".//span[@class='zg-badge-text']/text()")

            yield load.load_item()

