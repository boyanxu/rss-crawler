from typing import Any
import scrapy
import feedparser
from scrapy.http import Response
import trafilatura
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from utils.feed_helpers import is_feed, extract_all_links

class RssSpiderSpider(scrapy.Spider):
    name = "rss"
    def start_requests(self):
        print(os.getcwd())
        with open('smallweb.txt', 'r') as f:
            urls = [url.strip() for url in f.readlines()]
        for url in urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):
        # Parse the feed using feedparser
        if is_feed(response):

            feed = feedparser.parse(response.body)

            article_links = [entry.link for entry in feed.entries]
            yield from response.follow_all(article_links, self.parse_article, cb_kwargs={'rss_feed_url': feed.feed.link})

            # for entry in feed.entries:

            #     yield {
            #         'rss_feed_url': response.url,
            #         'article_link': entry.link,
            #     }


    def parse_article(self, response, rss_feed_url):

        fulltext = trafilatura.bare_extraction(response.body, favor_precision=False,
                                      include_comments=False, include_formatting=True,
                                      url= rss_feed_url,
                                      include_links=True)

        links = extract_all_links(fulltext['text'])
        # Yield new Scrapy requests for each link

        yield {
            'rss_feed_url': rss_feed_url,
            'article_link': response.url,
            'fulltext': fulltext['text'],
        }

        # for link in links:
        #     yield scrapy.Request(link['url'], callback=self.parse_link_page, cb_kwargs={'article_link': response.url})


    def parse_link_page(self, response, article_link):
        # yield {
        #     'rss_feed_url': response.meta['rss_feed_url'],
        #     'article_link': article_link,
        #     'link_page_link': response.url,
        # }
        pass
