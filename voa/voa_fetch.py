#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-21
# @Link        : www.diyidan.com
# @Version     : 1.0
# @Description : 爬取所有VOA内容


import requests
import time
import bs4
import random

from database.helper import DB_Session

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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

def get_mp3_download(target_url):
    if not target_url:
        return None
    response = requests.get(target_url)
    if response.status_code != 200:
        return None
    content = response.content
    if not content:
        return None
    return content

def get_url_bs4soup(target_url, target_headers):
    response = requests.get(target_url, headers=target_headers)
    if response.status_code != 200:
        return None
    html = response.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    if not soup:
        return None
    return soup


def get_all_voa_name_url_dict():

    vip_headers = get_vip_headers(host='www.51voa.com', referer='http://www.51voa.com/VOA_Special_English/')

    youku_movie_url_dict = {
        '常速': 'http://www.51voa.com/VOA_Standard_%d.html',
        # '慢速': 'http://v.qq.com/x/list/movie?cate=10001&offset=0&pay=100002&sort=18',
    }

    # def get_page_url(page):
    #     return '//list.youku.com/category/show/c_96_u_1_pt_1_s_1_d_1_p_1.html' % page

    name_url_fee_list = []
    for fee, url in youku_movie_url_dict.iteritems():
        origin_url = url
        for i in xrange(1, 200):
            url = origin_url % i
            soup = get_url_bs4soup(url, vip_headers)

            body = soup.find('div', id='list').ul
            if body:
                title_list = body.find_all('li')
            else:
                title_list = []
            for li in title_list:
                video_name = li.a.text
                video_url = li.a.get('href')
                if not video_url.startswith('http'):
                    video_url = 'http://www.51voa.com' + video_url
                if video_name and video_url:
                    # print video_url
                    name_url_fee_list.append((video_name, video_url, fee))

                    detail_soup = get_url_bs4soup(video_url, vip_headers)
                    video_mp3_url = None
                    if detail_soup.find('a', id='mp3'):
                        video_mp3_url = detail_soup.find('a', id='mp3').get('href')
                    # video_mp3 = get_mp3_download(video_mp3_url)
                    video_detail = detail_soup.find('div', id='content').text


                    # return (video_name, video_detail, video_mp3_url)

            print '%s-->第%s页' % (fee, i)

            # time.sleep(2)
    print 'Get name complete...' + '总计%d个' % len(name_url_fee_list)

    # # save to local txt
    # with open('qq_video_name_url_collect.txt', 'w') as f:
    #     f.write('\n'.join([','.join(list(x)) for x in name_url_fee_list]))
    #     f.close()
    #     print 'save to local txt complete!'

    # # save to datebase
    # session = DB_Session()
    # for x in name_url_fee_list:
    #     try:
    #         session.execute('insert into diyidan_youku_video_name_url (ykv_name, ykv_url, ykv_fee_type, ykv_source_type) values (:name, :url, :fee_type, :source_type)', {
    #                         'name': x[0], 'url': x[1], 'fee_type': x[2], 'source_type': 'qq'})
    #         session.commit()
    #     except:
    #         continue
    # print 'save to datebase complete...'


def get_all_leshi_video_name_url_dict():

    vip_headers = get_vip_headers(host='list.le.com', referer='http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph1_md_o2_d1_p.html')

    youku_movie_url_dict = {
        '免费': 'http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph1_md_o2_d1_p%d.html',
        '付费': 'http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph2_md_o2_d1_p%d.html',
    }

    # def get_page_url(page):
    #     return 'http://api.vip.le.com/search/interface?callback=jQuery19107210129822614852_1505962534578&from=pc_03&request_time=1505962534517&sales_area=cn&user_setting_country=cn&cg=1&ph=420001&pt=141001&dt=1&src=1&ispay=1&stype=1&lang=zh_cn&stt=1&ps=60&pn=1&lh=0&vt=180001&sc=&ar=&yr=&or=4&_=1505962534579' % page

    name_url_fee_list = []
    for fee, url in youku_movie_url_dict.iteritems():
        page_num = 1
        origin_url = url
        while url and page_num < 30:
            url = origin_url % page_num
            response = requests.get(url, headers=vip_headers)
            if response.status_code != 200:
                page_num += 1
                continue
            html = response.content
            soup = bs4.BeautifulSoup(html, 'html.parser')
            if not soup.find_all('p', class_='p_t'):
                page_num += 1
                continue
            for li in soup.find_all('p', class_='p_t'):
                video_name = li.a.get('title')
                video_url = li.a.get('href')
                if not video_url.startswith('http'):
                    video_url = 'http:' + video_url
                if video_name and video_url:
                    name_url_fee_list.append((video_name, video_url, fee))

            print '%s-->第%s页' % (fee, page_num)
            page_num += 1

            # time.sleep(5)
    print 'Get name complete...' + '总计%d个' % len(name_url_fee_list)

    # # save to local txt
    # with open('leshi_video_name_url_collect.txt', 'w') as f:
    #     f.write('\n'.join([','.join(list(x)) for x in name_url_fee_list]))
    #     f.close()
    #     print 'save to local txt complete!'

    # # save to datebase
    # session = DB_Session()
    # for x in name_url_fee_list:
    #     try:
    #         session.execute('insert into diyidan_youku_video_name_url (ykv_name, ykv_url, ykv_fee_type, ykv_source_type) values (:name, :url, :fee_type, :source_type)', {
    #                         'name': x[0], 'url': x[1], 'fee_type': x[2], 'source_type': 'leshi'})
    #         session.commit()
    #     except:
    #         continue
    # print 'save to datebase complete...'


if __name__ == '__main__':
    get_all_voa_name_url_dict()  # voa
