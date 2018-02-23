# coding:utf-8

"""
Created by lachang on 2018/2/5.
"""
import os
import urllib
import urlparse
from scrapy.mail import MailSender
from scrapy import log
from os.path import expanduser

from u2porn import settings
from u2porn.items import VideoDetail

home = expanduser("~")

DOWNLOAD_PATH = os.path.join(home, r"Desktop/video")


def get_search_url(original_url=None,
                   title=None,
                   tag_name=None,
                   page=1,
                   play_count=None,
                   release=None,
                   release_time=None):
    if original_url is not None:
        query = url_to_dict(original_url)
        for key in query.keys():
            if cmp(key, 'title') == 0 and title is None:
                title = query[key]
            elif cmp(key, 'tag_name') == 0 and tag_name is None:
                tag_name = query[key]
            elif cmp(key, 'page') == 0 and page is None:
                page = query[key]
            elif cmp(key, 'play_count') == 0 and play_count is None:
                play_count = query[key]
            elif cmp(key, 'release') == 0 and release is None:
                release = query[key]
            elif cmp(key, 'release_time') == 0 and release_time is None:
                release_time = query[key]

    if title is None: title = ''
    if tag_name is None: tag_name = ''
    if play_count is None: play_count = ''
    if release is None: release = ''
    if release_time is None: release_time = ''

    params = urllib.urlencode({'play_count': play_count,
                               'release': release,
                               'release_time': release_time,
                               'title': title,
                               'tag_name': tag_name,
                               'page': page
                               })

    return u'http://%s/v/search?%s' % (settings.HOST, params)


def url_to_dict(url):
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])


def get_detail_url(key):
    return r'http://%s/v/%s' % (settings.HOST, key)


def get_video_url(key):
    return r'http://media.vsteam.space/%s' % (key)


def mk_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        return path
    else:
        return None


def convert(list, detail):
    """
    转换
    :param list:
    :return:
    """
    item = VideoDetail()
    item['title'] = list.title
    item['access_lv'] = list.access_lv
    item['duration'] = list.duration
    item['id_encrypt'] = list.id_encrypt
    item['play_count'] = list.play_count
    item['timeout'] = list.timeout
    item['status'] = list.status
    item['thumb_href'] = list.thumb_href
    item['normal_key'] = detail.normal
    item['vip_key'] = detail.vip
    return item


def file_exists(filepath):
    filepath = filepath.strip()
    return os.path.exists(filepath)


def send_mail(title, message):
    mailer = MailSender()
    mailer.send(to=["someone@example.com"], subject=title, body=message)


def logging(msg=u""):
    # if isinstance(msg, 'unicode'):
    #     msg = msg.decode('utf-8')

    log.msg(msg, level=log.INFO)
    print msg


def get_keyword(spider, default='video'):
    title = None
    tag_name = None
    if hasattr(spider, 'arguments'):
        title = spider.arguments['title']
        tag_name = spider.arguments['tag_name']

    return title if title is not None else (tag_name if tag_name is not None else default)


def get_video_dir(subject):
    return unicode(os.path.join(DOWNLOAD_PATH, subject), encoding='utf-8')


def get_video_path(subject, meta):
    filename = u"%s_%s.mp4" % (meta['title'].replace(' ', ''), meta['id_encrypt'])
    filepath = os.path.join(get_video_dir(subject), filename)
    return filename, filepath
