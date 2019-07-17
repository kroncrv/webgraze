from webgraze.scraper import Scraper, ScrapeResults
from webgraze.utils import ZeroItems, to_number
import json
import logging

class HmScraper(Scraper):
    DOMAIN = "hm.com"
    NAME = "hm"
    PAGE_SIZE = 500

    def _parse_product(self, item):
        prod = {
            "articlecode" : item.get("data-articlecode"),
            "category" : item.get("data-category"),
            "href" : item.select("a")[0].get("href"),
            "heading" : item.select(".item-heading a")[0].get_text(),
            "price" : to_number(item.select(".item-price span")[0].get_text())
        }

        quality = item.select(".marker-quality")

        if len(quality) == 1:
            prod["quality"] = quality[0].get_text().strip()

        swatches = item.select(".list-swatches")

        if len(swatches) != 0:
            prod["swatches"] = [s.select(".swatch")[0].get("title") for s in swatches]

        return prod

    def _get_search(self, url):
        soup = self._get_soup(url)
        items = soup.select(".hm-product-item")

        if len(items) == 0:
            raise ZeroItems("No more items")

        return [self._parse_product(item) for item in items]

    def _get_soup(self, url):
        return super()._get_soup(url, headers = {
            "user-agent" : "Mozilla/5.0"
        })

    def _scrape_item(self):
        soup = self._get_soup(self.inp)
        ld = soup.select('script[type="application/ld+json"]')
        data = json.loads(ld[0].get_text())

        yield ScrapeResults(self.inp, data)

    def _scrape_paged(self):
        offset = 0

        while True:
            url = f"{self.inp}?offset={offset}&page-size={self.PAGE_SIZE}"

            try:
                data = self._get_search(url)
            except ZeroItems:
                logging.debug("No more pages, finishing up")
                break

            yield ScrapeResults(url, data)

            offset += self.PAGE_SIZE
            logging.debug(f"Setting next url: {url}")