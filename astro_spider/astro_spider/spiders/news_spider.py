# -*- coding: utf-8 -*-
import scrapy


class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['spacenews.com']
    start_urls = ['http://spacenews.com/section/commercial/', 'http://spacenews.com/section/launch/', 'https://spacenews.com/section/civil/']
    custom_settings = {'LOG_ENABLED': False,
    }

    def parse(self, response):
        for article_url in response.xpath("//h2[contains(@class, 'launch-title')]/a/@href").extract():
            yield response.follow(article_url, callback=self.parse_article)


    def parse_article(self, response):
        # Eliminating too small of paragraphs.

        bodyList = []

        # For each <p> Item found
        for i in response.xpath("//p//text()").getall():
            # Strip excess spaces
            i.strip()
            # IF the item is too small to stand alone.
            if len(i) < 200:
                # Don't add newlines or a tab
                bodyList.append(i)
            #but if it is the right size, add those things.    
            else:
                bodyList.append("\n\n\t" + i)

        article = {
            'title' : response.xpath("//h1[contains(@class, 'post-title')]//text()").extract()[0],
            'date'  : response.xpath("//time//text()").extract()[0],
            'body'  : " ".join(bodyList),
            'image'   : "".join(response.xpath("//figure[contains(@class, 'featured wp-caption')]//img/@src").extract())

        }


        #concatenate_list(article['body'])
        yield article
