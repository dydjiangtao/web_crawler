#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2017-09-16
# @Author      : Jiangtao Hu (hujiangtao@diyidan.com)
# @Link        : https://www.diyidan.com
# @Version     : 1.0
# @Description : 爬取所有优酷VIP视频名字


import requests
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    return 'http://vip.youku.com/ajax/filter/filter_data?tag=10005&pl=30&pt=1&ar=0&mg=0&y=0&cl=0&o=0&pn=%d' % page


name_list = []
for i in xrange(60):
    vip_url = get_page_url(i)
    response = requests.get(vip_url, headers=vip_headers, timeout=20)
    if response.status_code != 200:
        continue
    result_list = response.json().get('result').get('result') or []
    for x in result_list:
        name_list.append(x.get('showname'))

    # time.sleep(5)
print 'Get name complete...'

with open('vip_youku_video_name.txt', 'w') as f:
    f.write('\n'.join(name_list))
    f.close()
    print 'Done!'
