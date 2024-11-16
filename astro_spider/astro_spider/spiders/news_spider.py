# -*- coding: utf-8 -*-
import scrapy
import sqlite3, os
import unicodedata
from scrapy import Selector

class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['spacenews.com']
    start_urls = ['http://spacenews.com/section/commercial/', 'http://spacenews.com/section/launch/', 'https://spacenews.com/section/civil/']
    custom_settings = {'LOG_ENABLED': True,
    }

    def parse(self, response):

        for article_url in response.xpath("//h2[contains(@class, 'entry-title')]/a/@href").extract():
            yield response.follow(article_url, callback=self.parse_article)


    def parse_article(self, response):
       
        # Getting the body.

        bodyList = []
        div = response.xpath("//div[contains(@class, 'main-content')]//p//text()").extract()

        # Eliminating too small of paragraphs and excess whitespace added to the site in 2024
        for i in div: 
            # IF the item is too small to stand alone.
            if len(i) < 150:
                # Don't add newlines or a tab
                bodyList.append(" ".join(i.split()))
            #but if it is the right size, add those things.
            else:
                bodyList.append("\n\n\t" + " ".join(i.split()))




        imgTag = "".join(response.xpath("//figure[contains(@class, 'post-thumbnail')]/img/@src").extract())

        # trimming the found urls down to a single URL.
        if '.jpg' in imgTag:
            head, sep, tail = imgTag.partition('.jpg?')                                          # use partition() to seperate the item on the comma
            fixedImg = head.replace("https://i0.wp.com/", 'https://')+sep[:-1]
            
        elif '.jpeg' in imgTag:
            head, sep, tail = imgTag.partition('.jpeg?')                                          # use partition() to seperate the item on the comma
            fixedImg = head.replace("https://i0.wp.com/", 'https://')+sep[:-1]
            

        elif '.png' in imgTag:
            head, sep, tail = imgTag.partition('.png?')                                          # use partition() to seperate the item on the comma
            fixedImg = head.replace("https://i0.wp.com/", 'https://')+sep[:-1]
            
        else:
            fixedImg = imgTag

    

        article = {
            'title' : "".join(response.xpath("//h1[contains(@class, 'entry-title')]//text()").extract()).strip(),
            'date'  : response.xpath("//time[contains(@class, 'entry-date published')]/text()").extract()[-1],
            'body'  : " ".join(bodyList),
            'image'   : fixedImg

        }

        yield article
