# -*- coding: utf-8 -*-
import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookie.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie未能加载')

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'

headers = {
    'Host' : 'www.zhihu.com',
    'Referer' : 'https://www.zhihu.com/',
    'User-Agent' : user_agent
}

def get_xsrf():

    response = session.get("https://www.zhihu.com", headers=headers)

    print(response.text)

    matches = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if matches:
        return matches.group(1)
    else:
        return ''


def is_login():
    inbox_url = 'https://www.zhihu.com/settings/profile'
    response = session.get(inbox_url, headers = headers, allow_redirects = False)
    if response.status_code != 200:
        return False
    else:
        return True


def zhihu_login(account, password):
    if re.match("^1\d{9}", account):
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            "_xsrf" : get_xsrf(),
            "phone_num" : account,
            "password" : password
        }
        response_text = session.post(post_url, data=post_data, headers = headers)
        session.cookies.save()


zhihu_login('1581368456', '123456')

