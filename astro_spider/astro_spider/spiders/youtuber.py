# -*- coding: utf-8 -*-
import scrapy


class YoutuberSpider(scrapy.Spider):
    name = 'youtuber'
    allowed_domains = ['rocketlaunch.live']
    start_urls = ['https://www.rocketlaunch.live/?pastOnly=1&page=1']

    def parse(self, response):
        """
            Switched from getting launch videos from SpaceX's website, to getting it from the same source as the
            launch history spider.

            To-Do:
                Find a way to scrape only the first launch item to save resources.
                Merge this spider with LaunchhistorySpider.
        """
        link = response.xpath("//div[contains(@class, 'large-7 medium-6 large-push-3 medium-push-4 small-9 columns mission_name')]//a[contains(@class, 'mission_details_link async_link')]/@href").extract()[0]
        fullLink = 'https://www.rocketlaunch.live'+str(link) # Making the link useable
        yield response.follow(fullLink, callback=self.parse_launch)


    def parse_launch(self, response):

        videos = {
            'link' : response.xpath('//div[contains(@class, "columns large-7 medium-7")]//@src').extract()[0],
            'mission' : response.xpath('//div[contains(@class, "row header")]//text()').extract()[1]

        }

        yield videos
