# -*- coding: utf-8 -*-
import scrapy
import re

class HubblespiderSpider(scrapy.Spider):
    name = 'hubbleSpider'
    allowed_domains = ['spacetelescope.org', 'esawebb.org']
    start_urls = ['https://www.spacetelescope.org/images/potw/', 'https://esawebb.org/images/potm/']


    custom_settings = {'LOG_ENABLED': True, 'CONCURRENT_REQUESTS': '1'
    }


    def parse(self, response):
        start_urls = ['https://www.spacetelescope.org/images/potw/']
        halfhubUrl = 'https://www.spacetelescope.org'
        halfwebbUrl = 'https://esawebb.org'
        for pic_url in response.xpath("//div[contains(@class, 'col-md-3 col-sm-6 col-xs-12')]/a//@href").extract():
 
            full_url = halfhubUrl+pic_url

            yield response.follow(full_url, callback=self.parse_Potw, meta={'category': 'Hubble'})

        for pic_url in response.xpath("//div[contains(@class, 'col-lg-4 col-md-6 col-sm-12')]/a//@href").extract():

            full_url = halfwebbUrl+pic_url
            #print(full_url)
            
            if "comparisons" not in full_url:

                yield response.follow(full_url, callback=self.parse_webb, meta={'category': 'Webb'})

    def parse_Potw(self, response):

        # This gets ALL the child items from the div class 'missionData' and
        # merges all of the children into one beast and adds them to a library.
        descDat = []                # the lists that will ultimately be passed to potwData.
        headerData = []

        # Getting the category, this determines the telescope.
        telescope = response.meta['category']

        for r in response.xpath("//div[contains(@class, 'col-md-9 left-column')]"):
            fullDesc = [p.strip() for p in r.xpath('.//text()').extract() if p.strip()]
            descHeader = fullDesc[0]                    # Getting the first item found, this will be our header.
            headerData.append(descHeader)               # Appending it to a list

            fullDesc.pop(0)                             # popping the header off the list of <p> objects scraped


            # Fixing the format of the description. 
            
            betterSpaced = []

            for i in fullDesc:
                # Only newline and indent if over 200 characters
                if len(i) > 300:
                    betterSpaced.append("\n\n\t" + i)
                else:
                    betterSpaced.append(" " + i)        

            
            joinedDesc = " ".join(betterSpaced)             # combining all the found objects.
            head, sep, tail, = joinedDesc.partition('Credit:')  # Seperating the string by "Credit:"
            descDat.append(head)                        # Adding only everything from before "Credit:" to the list.


        # Fixing the found items in the xpath of the photo's metadata.
        # This ensures we only get the date of the image so they can be sorted.
        date =  response.xpath("//div[1]//tr[3]/td/text()").extract_first()                 # Just get the first item found, which will be the date.
        head, sep, tail = date.partition(', ')                                          # use partition() to seperate the item on the comma
        fixedDate = head                                                                # Getting the head, which is everything in front of the partition (the actual date)

        # Catches the object above where the date is supposed to be if it isn't
        # there. Prevents a parsing error in xNews module.
        if "px" in fixedDate or "heic" in fixedDate:
            date =  response.xpath("//tr[2]/td[2]//text()").extract_first()
            head, sep, tail = date.partition(', ')
            fixedDate = head
            



        potwData = {
            'telescope'   : telescope,
            'hubbleImage' : response.xpath("//img[contains(@class, 'img-responsive')]/@src").extract(),
            'header'      : headerData,
            'hubbleDescrip' : descDat,
            'hubbleDate' : fixedDate,
        }

        yield potwData

    def parse_webb(self, response):

        # Getting the category, this determines the telescope.
        telescope = response.meta['category']

        dateRow = response.xpath("//div[contains(@class, 'right-column')]//div[contains(@id, 'object_info_div')][1]//tr[3]/td/text()").extract_first()

        #print(dateRow)

        if dateRow == None:
            dateRow = response.xpath("//div[contains(@class, 'right-column')]//div[contains(@id, 'object_info_div')][1]//tr[2]/td/text()").extract_first()

        # Fixing the format of the description. 
        description = response.xpath("//p//text()").extract()
        betterSpaced = []

        for i in description:
            # Only newline and indent if over 200 characters
            if len(i) > 300:
                betterSpaced.append("\n\n\t" + i)
            else:
                betterSpaced.append(" " + i)        

        potwData = {
            'telescope'   : telescope,
            'hubbleImage' : response.xpath("//img[contains(@class, 'w-100')]/@src").extract(),
            'header'      : response.xpath("//div//h1//text()").extract(),
            'hubbleDescrip' : "".join(betterSpaced),
            'hubbleDate' :  "".join(dateRow),
        }

        #print(potwData['hubbleDescrip'])

        yield potwData
