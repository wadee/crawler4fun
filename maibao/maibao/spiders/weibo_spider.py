import scrapy
from http.cookies import SimpleCookie
import hashlib
import time
from urllib.parse import urlencode
import json


# reference from github repo : https://github.com/dataabc/weiboSpider

class WeiboSpider(scrapy.Spider):
    name = "weibo"

    def start_requests(self):
        return [scrapy.Request(
            "https://h5api.m.taobao.com/h5/mtop.mediaplatform.anchor.info/1.0/?jsv=2.4.8&appKey=12574478&t=1592031064516&sign=663ae11e16aeb0be30133aba0560ec66&api=mtop.mediaplatform.anchor.info&v=1.0&AntiCreep=true&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22broadcasterId%22%3A%221759494485%22%2C%22start%22%3A0%2C%22limit%22%3A10%7D",
            self.getCookie)]
    
    def assembleRequest(self, url):
        request = scrapy.Request(url,
            cookies = self.set_cookies,
            callback=self.parse)
        return request

    def postParse(self, response):
        # parse the dom

    def userInfoParse(self, response):
        return

    def commentParse(self):
        return ''

    def assemblePostUrl(self, uid):
        return 'https://weibo.cn/%s' % (uid)

    def newPostRequest(self, uid):
        url = self.assemblePostUrl(uid)
        request = scrapy.Request(url,
                                 cookies = self.cookie,
                                 callback=self.postParse)
        return request

    def config(self, config):
        self.cookie = config['cookie']
        self.uids = config['uids']
