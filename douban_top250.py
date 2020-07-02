'''
spider by pyspider

'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-22 20:08:47
# Project: hfut_news

from pyspider.libs.base_handler import *
from time import ctime
from hashlib import sha256


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://movie.douban.com/top250', callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#content > div > div.article > ol > li > div > div.info > div.hd > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)
        for each in response.doc('#content > div > div.article > div.paginator > span.next > a').items():
            self.crawl(each.attr.href, callback=self.index_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        ranking=response.doc('#content > div.top250 > span.top250-no').text()
        
        name=response.doc('#content > h1 > span:nth-child(1)').text()
        name_list=name.split(' ',1)    

        director_list=[]
        for each in response.doc('#info > span:nth-child(1) > span.attrs > a').items():
            director_list.append(each.text())
        
        screenwriter_list=[]
        for each in response.doc('#info > span:nth-child(3) > span.attrs > a').items():
            screenwriter_list.append(each.text())
        
        stars_list=[]
        for each in response.doc('.actor a ').items():
            stars_list.append(each.text())

        story_summary=response.doc('#link-report > span:nth-child(1)').text()


        score=response.doc('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong').text()

        url=response.url

        spider_time=ctime()

        Hash=sha256()
        Hash.update(ranking.encode('utf-8'))
        Hash.update(score.encode('utf-8'))
        for each in name_list:
            Hash.update(each.encode('utf-8'))
        for each in director_list:
            Hash.update(each.encode('utf-8'))
        for each in screenwriter_list:
            Hash.update(each.encode('utf-8'))
        for each in stars_list:
            Hash.update(each.encode('utf-8'))
        Hash.update(story_summary.encode('utf-8'))
        Hash.update(url.encode('utf-8'))
        Hash.update(spider_time.encode('utf-8'))
        H=Hash.hexdigest()
        
        return {
            "ranking":ranking,
            "score":score,
            "name":name_list,
            "director":director_list,
            "screenwriter":screenwriter_list,
            "stars":stars_list,
            "story_summary":story_summary,
            "url":url,    
            "spider_time":spider_time,
            "hash":H
        }