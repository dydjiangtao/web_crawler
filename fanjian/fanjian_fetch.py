#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-18
# @Version     : 1.0
# @Description : 爬取所有犯贱志的标题和正文(http://www.fanjian.net)

import os
import requests
import time
import bs4
import re

from multiprocessing import Pool as ThreadPool
from multiprocessing.dummy import Pool as ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(10000000)


total_count = 0
success_img_count = 0
fail_img_count = 0


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
            with open('fanjian_collect_2.txt', 'a') as f:
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


def get_imgs_and_save_to_local(fanjian):
    page_num = re.findall(r'Page-(\d+)', fanjian)
    if page_num:
        page_num = page_num[0]
    else:
        page_num = 'unknow'
    img_urls = re.findall(r'src="(\S+)"', fanjian)

    for url in img_urls:
        if not url.endswith('jpg') and not url.endswith('png') and not url.endswith('gif'):
            continue
        img_name = url.split('/')[-1]
        try:
            r = requests.get(url, stream=True)
            base_path = os.path.dirname(__file__)
            img_path = os.path.join(os.path.join(
                base_path, 'fanjian_imgs'), page_num)
            if not os.path.exists(img_path):
                os.mkdir(img_path)
            os.chdir(img_path)
            with open('%s' % img_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                f.close()

            global success_img_count
            success_img_count += 1
        except:
            global fail_img_count
            fail_img_count += 1
            continue

    print 'page-%s complete' % page_num


def get_fanjian_img_urls():
    for file in ['fanjian_collect.txt', 'fanjian_collect_2.txt']:
        with open(file, 'r') as f:
            content = f.read()
            fanjian_collect = re.split(r'\n{4}', content)
            print len(fanjian_collect)

            pool = ThreadPool(8)
            pool.map(get_imgs_and_save_to_local, fanjian_collect)
            pool.close()
            pool.join()

            f.close()

    print 'download: %s, fail: %s' % (success_img_count, fail_img_count)


if __name__ == '__main__':
    start = time.time()
    # get_fanjian_content()
    get_fanjian_img_urls()
    print '用时%s秒' % (round(time.time() - start, 3))
