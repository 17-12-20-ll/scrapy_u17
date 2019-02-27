# -*- coding: utf-8 -*-
import scrapy
import json
from u17.agent_helper import get_random_agent
from u17.items import U17Item


class ComicSpider(scrapy.Spider):
    name = 'comic'
    allowed_domains = ['www.u17.com']
    start_urls = ['http://www.u17.com/']

    def start_requests(self):
        """重新构造请求"""
        agent = get_random_agent()
        headers = {
            'Referer': 'http://www.u17.com/comic_list/th99_gr99_ca99_ss99_ob0_ac0_as0_wm0_co99_ct99_p1.html?order=2',
            'User-Agent': agent,
            'Host': 'www.u17.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
        }
        url = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'
        data = {
            'data[group_id]': 'no',
            'data[theme_id]': 'no',
            'data[is_vip]': 'no',
            'data[accredit]': 'no',
            'data[color]': 'no',
            'data[comic_type]': 'no',
            'data[series_status]': 'no',
            'data[order]': '2',
            'data[page_num]': 1,
            'data[read_mode]': 'no',
        }
        for page in range(1, 420):
            data['data[page_num]'] = str(page)
            yield scrapy.FormRequest(url=url,
                                     headers=headers,
                                     method='POST',
                                     formdata=data,
                                     callback=self.parse,
                                     )

    def parse(self, response):
        result_list = json.loads(response.text)
        for comic_item in result_list['comic_list']:
            u17_item = U17Item()
            u17_item['comic_id'] = comic_item['comic_id']
            u17_item['name'] = comic_item['name']
            u17_item['cover'] = comic_item['cover']
            u17_item['line2'] = comic_item['line2']
            yield u17_item
