# -*- coding: utf-8 -*-
import scrapy
import re
import json

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = ['http://zhihu.com/']


    headers = {
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
    }

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com', headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text
        matches = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        if matches:
            xsrf = matches.group(1)

            post_url = 'https://www.zhihu.com/login/phone_num'
            post_data = {
                "_xsrf": xsrf,
                "phone_num": '15829465509',
                "password": 'yangzie1137'
            }

            return [scrapy.FormRequest(
                url = post_url,
                formdata =post_data,
                headers = self.headers,
                callback=self.check_login
            )]

    def check_login(self, response):
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)



    def parse(self, response):
        pass
