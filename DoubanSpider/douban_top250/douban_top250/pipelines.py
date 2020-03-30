# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter


class DoubanTop250Pipeline(object):

    def __init__(self):
        self._file_path = './parse_result.json'
        self._file = None

    def open_spider(self, spider):
        self.file = open(self._file_path, 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        print(f"parse result is saved to {self._file_path}")

    def process_item(self, item, spider):
        #print(f"exporting item: {item}")
        self.exporter.export_item(item)
        return item
