# coding:utf-8

"""
Created by lachang on 2018/2/5.
"""

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl u2porn -a tag_name=嫩模".split())
