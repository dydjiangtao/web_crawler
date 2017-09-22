#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-18
# @Version     : 1.0
# @Description : 爬取所有犯贱志的标题和正文(http://www.fanjian.net)

import os
import requests
import time
import bs4

from multiprocessing import Pool as ThreadPool
from multiprocessing.dummy import Pool as ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(10000000)


total_count = 0


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

    def get_page_url_content(page_num):
        page_url = 'http://www.fanjian.net/post/%d' % page_num
        try:
            response = requests.get(page_url, headers=target_headers)
        except:
            time.sleep(2)
            return None
        if response.status_code != 200:
            return None
        html = response.content
        soup = bs4.BeautifulSoup(html, 'html.parser')
        try:
            title = soup.find('h1', class_='view-title').get('title')
        except:
            title = ''
        content = soup.find('div', class_='view-main') or ''
        if isinstance(content, bs4.Tag):
            content = str(content)

        # print '%s-->第%s页' % ('犯贱', page_num)
        global total_count
        total_count += 1
        print total_count

        return (title, content)

    fanjian_list = []

    # pool = ThreadPool(4)
    # fanjian = pool.map(get_page_url_content, xrange(1000, 125690))
    # pool.close()
    # pool.join()
    for i in xrange(1000, 125691):
        fanjian = get_page_url_content(i)
        if fanjian:
            fanjian_list.append(fanjian)

            # save to local txt
            with open('fanjian_collect.txt', 'a') as f:
                f.write('\n' * 4)
                f.write('Page-%d:\n' % i)
                f.write('\n\n'.join(fanjian))
                f.close()
                print 'save to local txt complete!'

    print 'Get fanjian complete...' + '总计%d个' % len(fanjian_list)

    # # save to local txt
    # with open('fanjian_collect.txt', 'w') as f:
    #     f.write(('\n' * 4).join(['\n\n'.join(list(x)) for x in fanjian_list]))
    #     f.close()
    #     print 'save to local txt complete!'


if __name__ == '__main__':
    start = time.time()
    get_fanjian_content()
    print '用时%s秒' % (round(time.time() - start, 3))
