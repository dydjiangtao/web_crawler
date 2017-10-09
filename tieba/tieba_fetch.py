#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-27
# @Version     : 1.0
# @Description : 爬取所有特定贴吧详情页的图片

import os
import requests
import time
import bs4
import re
import random

from multiprocessing import Pool as ThreadPool
from multiprocessing.dummy import Pool as ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(10000000)


total_count = 0
success_img_count = 0
fail_img_count = 0


def get_vip_headers(host, referer):

    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    ]

    VIP_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'close',
        'DNT': '1',
        'Host': host,
        'Referer': referer,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(USER_AGENTS),
    }
    return VIP_HEADERS


def get_url_bs4soup(target_url, target_headers):
    time.sleep(1)

    if not target_url.startswith('http'):
        target_url = 'http:' + target_url

    response = requests.get(target_url, headers=target_headers, timeout=200)
    if response.status_code != 200:
        return None
    html = response.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    if not soup:
        return None
    return soup


def get_tieba_detail():

    vip_headers = get_vip_headers(
        host='tieba.baidu.com', referer='https://tieba.baidu.com/')

    youku_movie_url_dict = {
        u'头像吧': 'http://tieba.baidu.com/f?ie=utf-8&kw=%E5%A4%B4%E5%83%8F',
        u'唯美图片吧': 'https://tieba.baidu.com/f?ie=utf-8&kw=%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87',
        u'动漫头像吧': 'https://tieba.baidu.com/f?ie=utf-8&kw=%E5%8A%A8%E6%BC%AB%E5%A4%B4%E5%83%8F',
        u'动漫图片': 'https://tieba.baidu.com/f?ie=utf-8&kw=%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87',
        u'欧美图片': 'https://tieba.baidu.com/f?ie=utf-8&kw=%E6%AC%A7%E7%BE%8E%E5%9B%BE%E7%89%87',
        u'二次元图片': 'https://tieba.baidu.com/f?ie=utf-8&kw=%E4%BA%8C%E6%AC%A1%E5%85%83%E5%9B%BE%E7%89%87',
    }

    name_url_fee_list = []
    for fee, url in youku_movie_url_dict.iteritems():
        page_num = 1
        while url:
            video_url_list = []
            soup = get_url_bs4soup(url, vip_headers)
            for li in soup.find_all('div', class_='threadlist_title'):
                video_name = li.a.get('title')
                video_url = li.a.get('href')
                if not video_url.startswith('https://tieba.baidu.com'):
                    video_url = 'https://tieba.baidu.com' + video_url
                if video_name and video_url:
                    video_url_list.append((fee, video_url))

            pool = ThreadPool(4)
            pool, map(get_page_detail_img_save, video_url_list)
            pool.close()
            pool.join()

            url = None
            if soup.find('a', text='下一页>'):
                url = soup.find('a', text='下一页>').get('href')

            print '%s-->第%s页已完成' % (fee, page_num)
            page_num += 1

    print 'Get name complete...' + '总计%d个' % len(name_url_fee_list)

    # pool = ThreadPool(4)
    # fanjian = pool.map(get_page_url_content, xrange(1000, 125690))
    # pool.close()
    # pool.join()


def get_page_detail_img_save(video_url):
    vip_headers = get_vip_headers(host='tieba.baidu.com', referer=video_url)
    fee = video_url[0]
    video_url = video_url[1]
    page_id = video_url.split('/')[-1]
    page_img_urls = []
    while video_url:
        detail_soup = get_url_bs4soup(video_url, vip_headers)
        for img in detail_soup.find_all('img', class_='BDE_Image'):
            detail_img_url = img.get('src')
            if detail_img_url:
                page_img_urls.append(detail_img_url)

        video_url = None
        if detail_soup.find('a', text='下一页'):
            video_url = detail_soup.find('a', text='下一页').get('href')
            if not video_url.startswith('https://tieba.baidu.com'):
                video_url = 'https://tieba.baidu.com' + video_url

        # 保存图片
        get_imgs_and_save_to_local(fee, page_id, page_img_urls)


def get_imgs_and_save_to_local(file_path, img_path, img_urls):

    try:
        base_path = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(base_path, file_path)):
            os.mkdir(os.path.join(base_path, file_path))
        img_path = os.path.join(os.path.join(
            base_path, file_path), img_path)
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        os.chdir(img_path)

        for url in img_urls:
            if not url.endswith('jpg') and not url.endswith('png') and not url.endswith('gif'):
                continue
            img_name = url.split('/')[-1]
            if os.path.exists(img_name):
                continue
            try:
                if not url.startswith('http'):
                    url = 'http:' + url
                r = requests.get(url, stream=True)
                with open('%s' % img_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                    f.close()
                    print url
                    print img_name

                global success_img_count
                success_img_count += 1

                time.sleep(0.2)
            except:
                global fail_img_count
                fail_img_count += 1
                continue

        print 'save complete Num.%d; failed:%d' % (success_img_count, fail_img_count)
    except:
        print 'Save failed --> %s' % img_path


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
    get_tieba_detail()
    # get_fanjian_img_urls()
    print '用时%s秒' % (round(time.time() - start, 3))
