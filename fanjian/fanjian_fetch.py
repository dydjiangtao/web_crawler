#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-18
# @Version     : 1.0
# @Description : 爬取所有犯贱志的标题和正文(http://www.fanjian.net)

import os
import requests
import time
import bs4

from multiprocessing.dummy import Pool as ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_fanjian_content():

    target_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.fanjian.net',
        'Referer': 'http://www.fanjian.net/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    def get_page_url(page):
        return 'http://www.fanjian.net/post/%d' % page

    def get_url_content(url):
        
        response = requests.get(url, headers=target_headers, timeout=20)
        if response.status_code != 200:
            return None
        html = response.content
        soup = bs4.BeautifulSoup(html, 'html5lib')
        try:
            title = soup.find('h1', class_='view-title').get('title')
        except:
            title = ''
        content = soup.find('div', class_='view-main') or ''
        if isinstance(content, bs4.Tag):
            content = str(content)

        return (title, content)

    target_url_list = []
    fanjian_list = []
    for i in xrange(1000, 1100):
        target_url_list.append(get_page_url(i))

    pool = ThreadPool(8)
    fanjian = pool.map(get_url_content, target_url_list)
    pool.close()
    pool.join()
    if fanjian:
        fanjian_list = fanjian

    # print '%s-->第%d页' % ('犯贱', i)

    print 'Get fanjian complete...' + '总计%d个' % len(fanjian_list)

    # save to local txt
    with open('fanjian_collect.txt', 'w') as f:
        f.write(('\n' * 4).join(['\n\n'.join(list(x)) for x in fanjian_list]))
        f.close()
        print 'save to local txt complete!'


if __name__ == '__main__':
    start = time.time()
    get_fanjian_content()
    print '用时%s秒' % (round(time.time()-start, 3))
