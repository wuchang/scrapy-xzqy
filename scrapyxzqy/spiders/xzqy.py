# -*- coding: utf-8 -*-
import scrapy
import os

class XzqySpider(scrapy.Spider):
    name = "xzqy"
    allowed_domains = ["www.stats.gov.cn"]
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/45.html']

    def parse(self, response):
        arrtr = response.xpath('//*[contains(@class, "tr")]')
        baseurl = os.path.dirname( response.url )
        for tr in arrtr:
            txt = tr.css("::text").extract()
            if len(txt) == 2:
                yield {'code': txt[0], 'name':txt[1]}
            else:
                yield {'code': txt[0], 'name':txt[2], 'type':txt[1]}

            lnks = tr.css("a::attr(href)").extract_first()
            if lnks:
                nextpath = '/'.join([baseurl,lnks])
                yield scrapy.Request( nextpath, callback=self.parse)
