import scrapy
import feedparser
import os
from utils.feed_helpers import is_feed

class RssSpiderSpider(scrapy.Spider):
    name = "rss"
    def start_requests(self):
        print(os.getcwd())
        with open('crawler_core/smallweb.txt', 'r') as f:
            urls = [url.strip() for url in f.readlines()]
        for url in urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):
        # Parse the feed using feedparser
        if is_feed(response):

            feed = feedparser.parse(response.body)

            for entry in feed.entries:

                yield {
                    'rss_feed_url': response.url,
                    'article_url': entry.link
                }


            # # Handling RSS feed
            # if root_element in ['rss', 'channel']:
            #     for item in response.xpath('//*[local-name()="item"]'):
            #         # Try extracting the link text
            #         article_url = item.xpath('.//*[local-name()="link"]/text()').get()
            #         # If the above doesn't work, try extracting the href attribute
            #         if article_url is None:
            #             article_url = item.xpath('.//*[local-name()="link"]/@href').get()
            #         yield {
            #             'rss_feed_url': response.url,
            #             'article_url': article_url
            #         }

            # # Handling Atom feed
            # elif root_element == 'feed':
            #     for entry in response.xpath('//*[local-name()="entry"]'):
            #         article_url = entry.xpath('*[local-name()="link" and @rel="alternate"]/@href').get()
            #         # If no URL is found, fall back to the more general XPath expression
            #         if article_url is None:
            #             article_url = entry.xpath('.//*[local-name()="link"]/@href').get()
            #         if article_url is None:
            #             article_url = entry.xpath('.//*[local-name()="link"]/text()').get()
            #         yield {
            #             'rss_feed_url': response.url,
            #             'article_url': article_url
            #         }

            # else:
            #     self.logger.error(f'Unknown feed type: {root_element}')


import json