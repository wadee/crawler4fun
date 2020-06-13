import scrapy
from http.cookies import SimpleCookie
import hashlib
import time
from urllib.parse import urlencode
import json


class TaobaoLiveSpider(scrapy.Spider):
    name = "taobaolive"
    cookie_m_h5_tk_value = ""
    cookie_m_h5_tk_key = "_m_h5_tk"
    set_cookies = {}
    token = ""
    appkey = "12574478"
    api_mtop_mediaplatform_anchor_info = "https://h5api.m.taobao.com/h5/mtop.mediaplatform.anchor.info/1.0/"

    def start_requests(self):
        return [scrapy.Request(
            "https://h5api.m.taobao.com/h5/mtop.mediaplatform.anchor.info/1.0/?jsv=2.4.8&appKey=12574478&t=1592031064516&sign=663ae11e16aeb0be30133aba0560ec66&api=mtop.mediaplatform.anchor.info&v=1.0&AntiCreep=true&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22broadcasterId%22%3A%221759494485%22%2C%22start%22%3A0%2C%22limit%22%3A10%7D",
            self.getCookie)]
    
    def getCookie(self, response):
        setCookie = response.headers.getlist('Set-Cookie')
        
        for ck in setCookie:
            ckStr = ck.decode("utf-8")
            cookie = SimpleCookie()
            cookie.load(ckStr)
            cookieDict = cookie.items()
            for k, v in cookieDict:
                if k == self.cookie_m_h5_tk_key:
                    self.cookie_m_h5_tk_value = v.value
                self.set_cookies[k] = v.value

        self.token = self.cookie_m_h5_tk_value.split("_")[0]
        # 1759494485 是主播uid - 李佳琪
        request = self.mtopMediaplatformAnchorInfo("1759494485")
        yield request

    def getSign(self, appKey, t, data):
        # data = '{"broadcasterId":"1759494485","start":0,"limit":10}'
        aR = self.token + "&" + str(t) + "&" + appKey + "&" + '{}'.format(data)
        sign = hashlib.md5(aR.encode()).hexdigest()
        return sign

    def mtopMediaplatformAnchorInfo(self, uid):
        t = int(round(time.time() * 1000))
        data = {
            'broadcasterId': uid,
            'start':0,
            'limit':10
        }
        dataStr = json.dumps(data,separators=(',', ':'))
        params = {
            'jsv':'2.4.8',
            'appKey':self.appkey,
            't':t,
            'sign':self.getSign(self.appkey, t, dataStr),
            'api':'mtop.mediaplatform.anchor.info',
            'v':'1.0',
            'AntiCreep':'true',
            'AntiFlood':'true',
            'type':'jsonp',
            'dataType':'jsonp',
            'callback':'mtopjsonp2',
            'data':dataStr,
        }
        urlWithQueryString = self.assembleUrlWithQueryString(self.api_mtop_mediaplatform_anchor_info, params)
        print("url : " +urlWithQueryString)
        request = self.assembleRequest(urlWithQueryString)
        return request

    def assembleRequest(self, url):
        request = scrapy.Request(url,
            cookies = self.set_cookies,
            callback=self.parse)
        return request

    def assembleUrlWithQueryString(self,url, params):
        return url + "?" + urlencode(params)

    def parse(self, response):
        print(response, response.body)
        body = str(response.body)
        body = body.lstrip('mtopjsonp2(')
        body = body.rstrip(')')
        print(body)