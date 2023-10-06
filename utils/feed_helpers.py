from scrapy.http import TextResponse
from lxml import etree
import re

def extract_markdown_links(text):
    # This regular expression captures patterns in the form of [TITLE](URL)
    # The first group captures the title, and the second group captures the URL.
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    # Using findall to get all matches as a list of tuples
    matches = re.findall(pattern, text)

    # Convert matches to a list of dictionaries for clearer representation
    return [{'url': url, 'title': title} for title, url in matches]

def extract_plain_links(text):
    # This regex captures URLs that are not part of the markdown link format.
    # The negative lookbehind (?<!\]\() ensures the URL isn't preceded by "](".
    # The negative lookahead (?!\)) ensures the URL isn't followed by ")".
    pattern = r'(?<!\]\()https?://\S+|www\.\S+(?!\))'

    # Using findall to get all matches as a list
    urls = re.findall(pattern, text)

    return [ {'url': url, 'title': ""} for url in urls]

def extract_all_links(text):
    return extract_markdown_links(text) + extract_plain_links(text)

def is_feed(response: TextResponse) -> bool:
    """
    Check if the response body is of a feed type (Atom, RSS2, RSS1, RSS0).

    Parameters:
    - response (TextResponse): A Scrapy response object.

    Returns:
    - bool: True if the response is a feed, otherwise False.
    """

    if not isinstance(response, TextResponse):
        return False

    try:
        root = etree.fromstring(response.body)

        # Check for Atom feed
        if root.tag == '{http://www.w3.org/2005/Atom}feed':
            return True

        # Check for various RSS feed types
        if root.tag == 'rss':
            # Check for version attribute to further narrow down
            version = root.get('version')
            if version in ['2.0', '1.0', '0.91', '0.92', '0.93', '0.94']:
                return True

        # Check for RDF (for RSS 1.0)
        if root.tag == '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF':
            return True

    except (etree.XMLSyntaxError, etree.XMLSchemaError):
        # Not a well-formed XML/Feed
        pass

    return False