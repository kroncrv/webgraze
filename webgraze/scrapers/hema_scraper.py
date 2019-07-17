"""
Overview page with only one page: https://www.hema.nl/dames/dameskleding/regenkleding
Overview page with two pages: https://www.hema.nl/dames/dameskleding/bikinis-badpakken
"""
from webgraze.scraper import Scraper, ScrapeResults
from webgraze.utils import ZeroItems, to_number
import html
import json
import logging

def parse_json(el):
    data = el.get("data-gtmproduct")
    return json.loads(html.unescape(data))

class HemaScraper(Scraper):
    DOMAIN = "hema.nl"
    NAME = "hema"

    def _get_overview(self, url):
        soup = self._get_soup(url)
        items = soup.select(".product-list .js-gtmproduct")
        parsed_items = [parse_json(item) for item in items]

        # Pages without a pager
        if len(soup.select(".paging")) == 0:
            return parsed_items, None
        else:
            next_url = soup.select(".paging .next")[0].get("href")
            return parsed_items, next_url

    def _scrape_item(self):
        soup = self._get_soup(self.inp)
        data_el = soup.select("#pdpMain")[0]
        yield ScrapeResults(self.inp, parse_json(data_el))

    def _scrape_paged(self):
        url = self.inp

        while True:
            data, next_url = self._get_overview(url)
            yield ScrapeResults(url, data)

            if not next_url:
                logging.debug("No more pages, finishing up")
                break
            else:
                url = next_url