# coding:utf-8

"""
Created by lachang on 2018/2/5.
"""


def SearchResult2Json():
    # (?<=xvideoData\.paginator\s=\s)(.+)(?=;xvideoData\.tags)
    pass


class SearchResult:
    """
    paginator:
    {
    "total": 235,
    "per_page": 30,
    "current_page": 1,
    "last_page": 8,
    "next_page_url": "/v/search?page=2",
    "prev_page_url": null,
    "from": 1,
    "to": 30,
    "data": []
    }
    """

    def __init__(self, js={}):
        if js is None: return
        self.total = js['total']
        self.per_page = js['per_page']
        self.current_page = js['current_page']
        self.last_page = js['last_page']
        self.next_page_url = js['next_page_url']
        self.prev_page_url = js['prev_page_url']
        self._from = js['from']
        self.to = js['to']
        videos = js['data']
        data = []
        if videos is not None and len(videos) > 0:
            for item in videos:
                data.append(VideoItem(item))

        self.data = data


class VideoItem:
    """
    {
            "id_encrypt": "z61rNXaP8hTOFHp3",
            "status": 10,
            "title": "",
            "timeout": "9个月前",
            "duration": "0:12:46",
            "thumb_href": "http://img.vquite.space/thumb/2017-04-04/Hu1Kok9IDM5nYiS0xPIn_thumb_6.jpg",
            "play_count": 22270,
            "access_lv": 0
        }
    """

    def __init__(self, js={}):
        if js is None or len(js) == 0: return
        self.id_encrypt = js['id_encrypt']
        self.status = js['status']
        self.title = js['title']
        self.timeout = js['timeout']
        self.duration = js['duration']
        self.thumb_href = js['thumb_href']
        self.play_count = js['play_count']
        self.access_lv = js['access_lv']


class VideoKey:
    """
    {"normal":"key-MjAxOC0wMi0xMi0wMy00OToyMDE2LTA3LTEzOm1DbEZxUHpmcWNCeldMZlRVZ3dzX05ELm1wNDpudWxsOmRBUmRjU1ZJNTRiY2JLSkFlbnJvVzBjYWRvRzhPRno1",
    "vip":"key-MjAxOC0wMi0xMi0wMy00OToyMDE2LTA3LTEzOm1DbEZxUHpmcWNCeldMZlRVZ3dzX05ELm1wNDozNS4xODUuMTMyLjE5MzpkQVJkY1NWSTU0YmNiS0pBZW5yb1cwY2Fkb0c4T0Z6NQ=="}
    """

    def __init__(self, js={}):
        if js is None: return
        self.normal = js['normal']
        self.vip = js['vip']


def main():
    import json
    maps = json.loads(r'''{
    "total": 235,
    "per_page": 30,
    "current_page": 1,
    "last_page": 8,
    "next_page_url": "/v/search?page=2",
    "prev_page_url": null,
    "from": 1,
    "to": 30,
    "data": [{
            "id_encrypt": "z61rNXaP8hTOFHp3",
            "status": 10,
            "title": "",
            "timeout": "9个月前",
            "duration": "0:12:46",
            "thumb_href": "http://img.vquite.space/thumb/2017-04-04/Hu1Kok9IDM5nYiS0xPIn_thumb_6.jpg",
            "play_count": 22270,
            "access_lv": 0
        }]}
    ''')
    page = SearchResult(maps)
    print type(maps)
    pass


if __name__ == '__main__':
    main()
