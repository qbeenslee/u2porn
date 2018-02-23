# coding:utf-8

"""
Created by lachang on 2018/2/5.
"""
import json

from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from u2porn import settings
from u2porn.jsons import SearchResult, VideoKey
from u2porn.utils import get_search_url, get_detail_url, convert, logging


class U2PornSpider(CrawlSpider):
    name = 'u2porn'
    allowed_domains = [settings.HOST, r'media.vsteam.space']

    def __init__(self, title=None, tag_name=None, url=None, *a, **kw):
        super(U2PornSpider, self).__init__(*a, **kw)
        if url is not None:
            #TODO
            self.arguments = {'url': url}
            self.start_urls = [url]
        elif title is not None or tag_name is not None:
            logging('搜索: title=%s  tag_name=%s' % (title, tag_name))
            self.arguments = {'title': title, 'tag_name': tag_name}
            self.start_urls = [get_search_url(title=title, tag_name=tag_name, page=1)]
        else:
            self.start_urls = [get_search_url(title='', page=1)]

    def parse(self, response):
        """
        生成循环
        :param response:
        :return:
        """
        js = response.selector.re(r'(?<=xvideoData\.paginator\s=\s)(.+)(?=;xvideoData\.tags)')
        if js is not None:
            result = SearchResult(json.loads(js[0]))
            if result is None: return
            logging(u"视频数量: %s" % result.total)
            for video in result.data:
                yield Request(
                        url=get_detail_url(video.id_encrypt),
                        meta={'video_meta': video},
                        callback=self.parse_detail
                )

            for index in range(result.current_page, result.last_page):
                next_page = index + 1
                yield Request(url=get_search_url(original_url=response.url, page=next_page), callback=self.parse_list)

    def parse_list(self, response):
        """
        解析列表
        :param response:
        :return:
        """
        js = response.selector.re(r'(?<=xvideoData\.paginator\s=\s)(.+)(?=;xvideoData\.tags)')
        if js is not None:
            result = SearchResult(json.loads(js[0]))
            if result is None and (result.data is None or len(result.data) <= 0): return

            for video in result.data:
                yield Request(
                        url=get_detail_url(video.id_encrypt),
                        meta={'video_meta': video},
                        callback=self.parse_detail
                )

    def parse_detail(self, response):
        """
        解析视频播放页
        :param response:
        :return:
        """
        video_meta = response.meta['video_meta']

        js = response.selector.re(r'(?<=xvideoData\.keys\s=\s)(.+)(?=;xvideoData\.is_dash)')
        if js is not None:
            key = VideoKey(json.loads(js[0]))
            yield convert(video_meta, key)
