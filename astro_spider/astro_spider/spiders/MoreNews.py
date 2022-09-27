# -*- coding: utf-8 -*-
import scrapy
import re

class MorenewsSpider(scrapy.Spider):
    name = 'MoreNews_spider'
    allowed_domains = ['space.com']
    start_urls = ['https://www.space.com/tech-robots', 'https://www.space.com/science-astronomy']
    custom_settings = {'LOG_ENABLED': True,
    }

    def parse(self, response):
        for article_url in response.xpath("//a[contains(@class, 'article-link')]//@href").extract():
            yield response.follow(article_url, callback=self.parse_article)


    def parse_article(self, response):

        # Fixing the found items in the xpath of the photo's metadata.
        # This ensures we only get the date of the image so they can be sorted.
        date =  "".join(response.xpath("//div[contains(@class, 'byline')]//time//text()").extract())                 # Just get the first item found, which will be the date.
        head, sep, tail = date.partition('T')                                          # use partition() to seperate the item on the comma
        fixedDate = head                                                                # Getting the head, which is everything in front of the partition (the actual date)


        bodyItems = [i.strip() for i in response.xpath("//div[contains(@class, 'text-copy bodyCopy auto')]/p[not(.//strong)]//text()").getall()]
        
        # Getting the different types of possible images
        mainImage = "".join(response.xpath("//div[contains(@class, 'box')]//img/@src").extract())
        altImage  = response.xpath("//img[contains(@class, 'expandable lazy-image-van')]/@data-srcset").get()
        thirdImage  = response.xpath("//img[contains(@class, 'block-image-ads hero-image')]//@src").get()

        #print(mainImage)
        # If the page doen't have one format of an image, try the other format.
        if mainImage == "/media/img/missing-image.svg":
            imageUsed = altImage

   
        elif mainImage is None or altImage is None and thirdImage is not None:
            imageUsed = thirdImage

            
        else:
            imageUsed = mainImage


        # trimming the found urls down to a single URL.
        if '.jpg' in str(imageUsed):
            head, sep, tail = imageUsed.partition('.jpg')                                          # use partition() to seperate the item on the comma
            fixedImg = head+sep

        elif '.jpeg' in str(imageUsed):
            head, sep, tail = imageUsed.partition('.jpeg')                                          # use partition() to seperate the item on the comma
            fixedImg = head+sep

        elif '.png' in str(imageUsed):
            head, sep, tail = imageUsed.partition('.png')                                          # use partition() to seperate the item on the comma
            fixedImg = head+sep
        
        else:
            fixedImg = imageUsed


        # Fixing the spacing of the items, so smaller items don't get indented.
        betterSpaced = []



        for i in bodyItems:
            # Only newline and indent if over 200 characters
            if len(i) > 200:
                betterSpaced.append("\n\n\t" + i.replace("(opens in new tab)", ""))
            else:
                betterSpaced.append(" " + i.replace("(opens in new tab)", ""))




        """
            Attempting to scrape video objects from Space.com articles.
            Added V0.90 Beta
        """
        """
        isVid = False
        vidScrape = response.xpath("/html/body/div[2]/article/section/div[1]/div[4]/div/div/script").extract()
        youtubeURL = response.xpath("//div//iframe//@src").extract()
        #print(vidScrape)
        
        if len(vidScrape) == 0 and len(youtubeURL) == 0:
            isVid  = False
            vidUrl = "Blank"

        elif len(vidScrape) != 0:
            isVid = True
            vidUrl = vidScrape[0]

        elif len(youtubeURL) != 0:
            isVid = True
            vidUrl = youtubeURL[0]
        """
        article = {
            'title' : "".join(response.xpath("//h1//text()").extract()),
            'date'  : fixedDate,
            'body'  : "".join(betterSpaced),
            'image'   : fixedImg,

        }


        yield article

