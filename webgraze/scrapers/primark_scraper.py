from webgraze.scraper import Scraper, ScrapeResults
from webgraze.utils import ZeroItems, to_number
import html
import json
import logging

class PrimarkScraper(Scraper):
    DOMAIN = "primark.com"
    NAME = "primark"

    def _get_search(self, url):
        soup = self._get_soup(url)
        items = soup.select(".product-listing__item")

        if len(items) == 0:
            raise ZeroItems("No more items")

        return [self._parse_product(item) for item in items]

    def _get_soup(self, url):
        return super()._get_soup(url, headers = {
            "Accept-Language" : "nl"
        })

    def _parse_product(self, item):
        price = item.select(".product-item__price")[0].get_text()

        prod = {
            "name" : item.select(".product-item__name a")[0].get_text().strip(),
            "href" : item.select(".product-item__name a")[0].get("href"),
            "price" : to_number(price)
        }

        return prod

    def _scrape_item(self):
        soup = self._get_soup(self.inp)

        data_raw = soup.select(".gallery [data-options]")[0].get("data-options")
        data = html.unescape(data_raw)
        data = json.loads(data)
        product_id = soup.select(".product-panel__id p")[0].get_text()

        yield ScrapeResults(self.inp, {
            "set" : data["set"],
            "name" : data["product"]["name"],
            "description" : data["product"]["description"],
            "price" : to_number(data["product"]["price"]),
            "product_id" : to_number(product_id)
        })

    def _scrape_paged(self):
        page = 0

        while True:
            if "?q=" in self.inp:
                url = f"{self.inp}&page={page}"
            else:
                url = f"{self.inp}?q=%3Arelevance&page={page}"

            try:
                data = self._get_search(url)
            except ZeroItems:
                logging.debug("No more pages, finishing up")
                break

            yield ScrapeResults(url, data)

            page += 1
            logging.debug(f"Setting next url: {url}")