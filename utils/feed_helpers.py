from scrapy.http import TextResponse
from lxml import etree

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