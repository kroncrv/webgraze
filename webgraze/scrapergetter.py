from urllib.parse import urlparse
from .utils import get_domain_from_url
import logging
import re
import webgraze.scrapers as scraper_modules

def get_scraper(url):
    domain = get_domain_from_url(url)
    # FIXME: subdomains should work here as well,
    # or maybe a way to do a regex instead of just a domain
    logging.debug(f"Getting scraper for domain {domain}")

    for cls in scraper_modules.__all__:
        if re.search(cls.DOMAIN, domain) != None:
            return cls

    raise Exception(f"Could not find scraper for <{url}>")

def get_scraper_by_name(name):
    for cls in scraper_modules.__all__:
        if cls.NAME == name:
            return cls

    raise Exception(f"Could not find scraper with name <{name}>")