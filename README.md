# RSS Crawler README

## Overview

This Scrapy spider is designed to crawl RSS feeds and extract articles from the corresponding feeds. It leverages both the `feedparser` library for parsing RSS feed entries and the `trafilatura` library to extract detailed information from the linked articles.

## Features

- **RSS Feed Parsing**: Parses RSS feeds to extract article links.
- **Article Content Extraction**: Extracts the full text of articles using `trafilatura`, including relevant metadata.
- **Link Extraction**: Extracts all links present within the article's content.

## How to Use

1. **Prerequisites**:

   - Ensure you have `scrapy`, `feedparser`, and `trafilatura` libraries installed.

2. **URLs Source File**:

   - Create a `smallweb.txt` file at the root of the `crawler_core` directory.
   - Populate this file with one URL (RSS feed URL) per line.

3. **Run the Spider**:

   - Navigate to the root of the `crawler_core` directory in your terminal.
   - Run the following command:

     ```bash
     scrapy crawl rss
     ```

4. **Output**:

   - As the spider runs, it will yield a dictionary for each article with the following fields:
     - `rss_feed_url`: The RSS feed's URL.
     - `article_link`: The direct link to the article.
     - `fulltext`: The extracted full text of the article.

## Code Structure

- `start_requests` Method: Reads the `smallweb.txt` file to get a list of RSS feed URLs and starts the crawling process.

- `parse` Method: Processes the fetched RSS feed, parses it, and follows the links to the articles.

- `parse_article` Method: Extracts the full text of the fetched articles and any embedded links.

- `parse_link_page` Method: A placeholder method that can be further developed to process pages linked within articles.

## Dependencies

- **feedparser**: Parses the RSS feed to extract article URLs.
- **trafilatura**: Extracts detailed content from the articles.
- **Scrapy**: Provides the framework for the web crawling.

## Extending the Spider

The spider is designed with modularity in mind. You can easily:

- **Extend Link Processing**: Uncomment the relevant sections in `parse_article` and `parse_link_page` methods to further process or extract details from links found within articles.
- **Add More Callbacks**: Define additional parsing methods and link them using Scrapy's callback mechanism.

## Notes

Make sure to respect `robots.txt` files of websites you crawl and ensure you're adhering to the terms of service of the websites you're accessing.

---

I hope this README provides a clear overview and instructions for your RSS Crawler! If you have additional functionalities or requirements in the future, be sure to update the README accordingly.