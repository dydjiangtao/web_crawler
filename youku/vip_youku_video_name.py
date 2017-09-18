#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-18
# @Author      : Jiangtao Hu (hujiangtao@diyidan.com)
# @Link        : www.diyidan.com
# @Version     : 1.0
# @Description : 爬取所有优酷VIP视频名字
# @Changes     : 1,爬取所有优酷电影 名字 -- 详情url -- 是否会员限制


import requests
import time
import bs4

from database.helper import DB_Session

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_vip_youku_video_name_list():

    vip_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__ysuid=1503561665116vLI; __yscnt=1; __arycid=dc-3-2034-2050; __arcms=dc-3-2034-2050; ypvid=1505540985663IWfYAz; yseid=1505540985664LUyWxL; ysestep=1; yseidcount=1; yseidtimeout=1505548185664; ycid=0; ystep=1; juid=01bq4jokq31toc; seid=01bq4jokq42su4; referhost=http%3A%2F%2Fvip.youku.com; seidtimeout=1505542785668; P_ck_ctl=D38216493264A1B3720B352FCFE185AD; _m_h5_tk=a71c8441efddf621456d7296ac1df93a_1505544566020; _m_h5_tk_enc=7f5ab3f6a90b9cd1009bc2064b483656; PHPSESSID=6ots7oujoanvu03eu4vbpb2t37; __ayvstp=10; __aysvstp=8; cna=B3clEtDJG2UCAbSt2RBrzXxq; __ayft=1503891224000; __aysid=1505540904643ShF; __arpvid=1505543117251UjMcUo-1505543117255; __ayscnt=1; __aypstp=10; __ayspstp=10; isg=AhAQz4JvfS8FdSErAfls7HYT4V6icfaqc8AsAgrh3Gs-RbDvsunEs2Y1Yzte',
        'DNT': '1',
        'Host': 'vip.youku.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    # vip_url = 'http://vip.youku.com/vips/TV.html?spm=a2h03.8173536.2100224.1&tag=10005&pt=1&ar=0'
    # 页面初步加载基本框架，ajax异步请求单独接口填充视频信息框

    def get_page_url(page):
        return 'http://vip.youku.com/ajax/filter/filter_data?tag=10005&pl=30&pt=1&ar=6&mg=0&y=0&cl=1&o=0&pn=%d' % page

    name_url_fee_list = []
    for i in xrange(60):
        vip_url = get_page_url(i)
        response = requests.get(vip_url, headers=vip_headers, timeout=20)
        if response.status_code != 200:
            continue
        result_list = response.json().get('result').get('result') or []
        for x in result_list:
            video_name = x.get('showname')
            video_url = x.get('firstepisode_videourl')
            if not video_url.startswith('http'):
                video_url = 'http:' + video_url
            name_url_fee_list.append((video_name, video_url, '付费'))

        print '%s-->第%s页' % ('vip', i)

        # time.sleep(5)
    print 'Get name complete...' + '总计%d个' % len(name_url_fee_list)

    # save to local txt
    with open('youku_video_name_url_collect_vip.txt', 'w') as f:
        f.write('\n'.join([','.join(list(x)) for x in name_url_fee_list]))
        f.close()
        print 'save to local txt complete!'


def get_all_youku_video_name_url_dict():

    vip_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': '__ysuid=1503561665116vLI; __yscnt=1; juid=01bq4jokq31toc; _uab_collina=150554468319151165278353; yseid=1505699125772nI7JwX; yseidcount=2; seid=01bq9aimgf15nn; referhost=http%3A%2F%2Fyouku.com; premium_cps=3031292176__54%7C401%7C83375%7C3107__; rpvid=1505699175785APmy07-1505699179776; __utmarea=; ykss=8c25bf59123e05d94e18fe29; _m_h5_tk=332639829da1fc6d85e2fcf18b35355b_1505704252248; _m_h5_tk_enc=64ec5ae1a76da4df749fb269428a36dd; __ayvstp=2; __aysvstp=15; __arycid=cms-00-11254-26704-0; __arcms=cms-00-11254-26704-0; _zpdtk=037e6be8a15bb19dc3e8d6475992a97c4e00c494; ypvid=1505701253747Q4gbAL; ysestep=53; yseidtimeout=1505708453748; ycid=0; ystep=59; seidtimeout=1505703053751; filter_status=show; cna=B3clEtDJG2UCAbSt2RBrzXxq; __ayft=1505699125634; __aysid=1505540904643ShF; __arpvid=1505701253890feOXuh-1505701253895; __ayscnt=1; __aypstp=57; __ayspstp=81; P_ck_ctl=DB583793E9B313D3FFD2F7FA5E1A5F57; _umdata=70CF403AFFD707DFA12976C96A0A03CEED50E371150C4D1FD2E987DEDCC77BD731A6B11130C74410CD43AD3E795C914C718CE6D1362F2730B950EC7DD1D24381; isg=AhkZN5KHpDdI1XigEFblx7fUKAUzDg_RkudVyTvOZcC7QjjV1PaDKDYUOjDP',
        'DNT': '1',
        'Host': 'list.youku.com',
        'Referer': 'http://list.youku.com/category/show/c_96_u_1_pt_0_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!6~1~3~A',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    # vip_url = 'http://vip.youku.com/vips/TV.html?spm=a2h03.8173536.2100224.1&tag=10005&pt=1&ar=0'
    # 页面初步加载基本框架，ajax异步请求单独接口填充视频信息框

    youku_movie_url_dict = {
        '免费': 'http://list.youku.com/category/show/c_96_u_1_pt_1_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!6~1~3!2~A',
        '付费': 'http://list.youku.com/category/show/c_96_u_1_pt_2_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!6~1~3!3~A',
        '点播': 'http://list.youku.com/category/show/c_96_u_1_pt_3_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!6~1~3!4~A',
        '包月': 'http://list.youku.com/category/show/c_96_u_1_pt_4_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!6~1~3!5~A',
    }

    # def get_page_url(page):
    #     return '//list.youku.com/category/show/c_96_u_1_pt_1_s_1_d_1_p_1.html' % page

    name_url_fee_list = []
    for fee, url in youku_movie_url_dict.iteritems():
        if fee in ['付费', '点播', '包月']:
            fee = '付费'
        page_num = 1
        while url:
            response = requests.get(url, headers=vip_headers, timeout=20)
            if response.status_code != 200:
                continue
            html = response.content
            soup = bs4.BeautifulSoup(html, 'html5lib')
            for li in soup.find_all('li', class_='title'):
                video_name = li.a.get('title')
                video_url = li.a.get('href')
                if not video_url.startswith('http'):
                    video_url = 'http:' + video_url
                name_url_fee_list.append((video_name, video_url, fee))

            url = None
            if soup.find('li', class_='next').a:
                url = soup.find('li', class_='next').a.get('href')
                if not url.startswith('http'):
                    url = 'http:' + url

            print '%s-->第%s页' % (fee, page_num)
            page_num += 1

            # time.sleep(5)
    print 'Get name complete...' + '总计%d个' % len(name_url_fee_list)

    # save to local txt
    with open('youku_video_name_url_collect.txt', 'w') as f:
        f.write('\n'.join([','.join(list(x)) for x in name_url_fee_list]))
        f.close()
        print 'save to local txt complete!'


if __name__ == '__main__':
    get_all_youku_video_name_url_dict()
    get_vip_youku_video_name_list()
