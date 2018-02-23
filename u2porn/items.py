# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoDownload(scrapy.Item):
    """
    下载
    """
    title = scrapy.Field()
    key = scrapy.Field()


class VideoDetail(scrapy.Item):
    """
    视频详细信息
    """
    id_encrypt = scrapy.Field()
    status = scrapy.Field()
    title = scrapy.Field()
    timeout = scrapy.Field()
    duration = scrapy.Field()
    thumb_href = scrapy.Field()
    play_count = scrapy.Field()
    access_lv = scrapy.Field()
    normal_key = scrapy.Field()
    vip_key = scrapy.Field()
