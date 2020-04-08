# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ..items import Book


class DoubanBookTop250Spider(scrapy.Spider):
    name = 'douban_book_top250'
    allowed_domains = ['douban.com']
    start_urls = ['https://douban.com/']

    def start_requests(self):
        for i in range(0, 10):
            url = f"https://book.douban.com/top250?start={i*25}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(f"parsing url: {response.url}")
        selector = etree.HTML(response.text)
        book_list = selector.xpath("//div[@class='pl2']")
        for book in book_list:
            item = Book()
            title = book.xpath("a/text()")[0].strip()
            link = book.xpath("a/@href")[0].strip()
            # print(link)
            # print(title)
            item["title"] = title
            item["link"] = link
            yield scrapy.Request(url=link, callback=self.parse_detail, meta={"item": item, 'dont_redirect': True,
                                                                             'handle_httpstatus_list': [302]})

    def parse_detail(self, response):
        item = response.meta["item"]
        print(f"parse detail: {response.url}")
        selector = etree.HTML(response.text)
        author_list = selector.xpath(
            "//div[@id='info']//span/a/text()")
        item["author"] = "|".join(author_list)
        item["rating"] = selector.xpath(
            "//*[@id='interest_sectl']//strong/text()")[0].strip()
        # print(item)
        yield item
