# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.media import MediaPipeline

from u2porn.utils import mk_dir, get_video_url, file_exists, logging, get_keyword, get_video_dir, get_video_path


class BloomFilterPipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        super(JsonWriterPipeline, self).__init__()
        self.__json_file__ = None
        self.seed = set()

    def open_spider(self, spider):
        filename = get_keyword(spider)
        self.__json_file__ = open('%s.json' % filename, 'wb')
        self.__json_file__.write("[\n")

    def close_spider(self, spider):
        self.__json_file__.write("]\n")
        self.__json_file__.close()

    def process_item(self, item, spider):
        if item['id_encrypt'] in self.seed:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seed.add(item['id_encrypt'])
            line = json.dumps(dict(item)) + ",\n"
            self.__json_file__.write(line)
            return item


class FilesPipeline(MediaPipeline):
    def __init__(self, download_func=None, settings=None):
        super(FilesPipeline, self).__init__(download_func, settings)
        self.failure_log = None
        self.keyword = None

    def open_spider(self, spider):
        super(FilesPipeline, self).open_spider(spider)
        self.failure_log = open('failure.json', 'wb')
        self.keyword = get_keyword(spider)
        mk_dir(get_video_dir(self.keyword))

    def close_spider(self, spider):
        self.failure_log.close()

    def get_media_requests(self, item, info):
        filename, filepath = get_video_path(self.keyword, item)

        if file_exists(filepath):
            raise DropItem(u'%s 已存在' % filename)

        normal_key = item['normal_key']
        vip_key = item['vip_key']
        key = vip_key if isinstance(vip_key, basestring) else normal_key
        url = get_video_url(key)
        request = scrapy.Request(
                url=url,
                method="GET",
                meta={"item": item, 'download_timeout': 18000},
        )
        return request

    def media_downloaded(self, response, request, info):
        filename, filepath = get_video_path(self.keyword, response.meta['item'])

        with open(filepath, "wb") as f:
            f.write(response.body)

        logging(u"%s" % filename)

    def media_failed(self, failure, request, info):
        item = request.meta['item']
        filename, filepath = get_video_path(self.keyword, item)

        logging(u"==========\n%s 失败" % filename)

        line = json.dumps(dict(item)) + "\n"
        self.failure_log.write(line)
