# -*- coding: utf-8 -*-
import scrapy
import sqlite3, os

class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['spacenews.com']
    start_urls = ['http://spacenews.com/section/commercial/', 'http://spacenews.com/section/launch/', 'https://spacenews.com/section/civil/']
    custom_settings = {'LOG_ENABLED': True,
    }

    def parse(self, response):
        """
        # If the database file doesn't already exist.
        if not os.path.isfile(os.path.expanduser("~/.AstroNinja/AstroData.db")):

            # Creating the Database
            datConn = sqlite3.connect(os.path.expanduser("~/.AstroNinja/AstroData.db"))

            datCurse = datConn.cursor()

            # Creating the articles table in the database
            sql_create_articles_table =  CREATE TABLE IF NOT EXISTS articles (
                                        id integer PRIMARY KEY,
                                        url text,
                                        Title text,
                                        Date text,
                                        image text,
                                        body text
                                    );

            datCurse.execute(sql_create_articles_table)

            """
        for article_url in response.xpath("//h2[contains(@class, 'entry-title')]/a/@href").extract():
            yield response.follow(article_url, callback=self.parse_article)

        # If the database file does already exist.
        """elif os.path.isfile(os.path.expanduser("~/.AstroNinja/AstroData.db")):

            # Creating the Database
            datConn = sqlite3.connect(os.path.expanduser("~/.AstroNinja/AstroData.db"))

            'datCurse = datConn.cursor()

            # Getting all the urls from the database.

            datCurse.execute("SELECT url FROM articles")
            urls = datCurse.fetchall()
            for article_url in response.xpath("//h2[contains(@class, 'launch-title')]/a/@href").extract():
                if article_url in urls:
                    return

                elif article_url not in urls:
                    artIn = (article_url)
                    sqlInsert =  INSERT INTO articles(url)
                                    VALUES(?,) 

                    datCurse.execute(sqlInsert, artIN)
                    datConn.commit()
                    print(article_url)

                    yield response.follow(article_url, callback=self.parse_article)"""

    def parse_article(self, response):
        # Eliminating too small of paragraphs.

        bodyList = []

        # For each <p> Item found
        for i in response.xpath("//div[contains(@class, 'entry-content')]//p//text()").getall():
            # Strip excess spaces
            i.strip()
            # IF the item is too small to stand alone.
            if len(i) < 200:
                # Don't add newlines or a tab
                bodyList.append(i)
            #but if it is the right size, add those things.
            else:
                bodyList.append("\n\n\t" + i)


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
