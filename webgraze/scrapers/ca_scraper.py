from bs4 import BeautifulSoup
from webgraze.scraper import Scraper, ScrapeResults
from webgraze.utils import ZeroItems, to_number
import logging
import requests

class CaScraper(Scraper):
    DOMAIN = "c-and-a.com"
    NAME = "ca"

    def _get_overview(self, url):
        # We do the whole request here, because we need the request to check
        # for a 302, which means there are no more pages
        logging.debug(f"Getting <{url}>")
        req = requests.get(url, allow_redirects = False)

        if req.status_code != 200:
            raise ZeroItems("No more items")

        logging.debug(f"Got <{url}>")
        soup = BeautifulSoup(req.text, features = "lxml")
        self.last_html = str(soup)

        items = soup.select(".product-tile")

        return [self._parse_product(item) for item in items]

    def _parse_product(self, item):
        # First check if there's a sale price
        if len(item.select(".product-tile__price--new")) > 0:
            price = item.select(".product-tile__price--new")
        else:
            price = item.select(".product-tile__price span")

        price = to_number(price[0].get_text())
        colors = [i.get("title") for i in item.select(".color-list__img-wrapper img")]

        prod = {
            "colors" : colors,
            "fulltitle" : item.get("title"),
            "href" : item.select("a")[0].get("href"),
            "price" : price,
            "productid" : item.get("data-productid"),
            "title" : item.select(".product-tile__title")[0].get_text()
        }

        return prod

    def _scrape_item(self):
        soup = self._get_soup(self.inp)
        brand, title = soup.select(".product-stage__title")[0].get_text().split("\n")

        yield ScrapeResults(self.inp, {
            "brand" : brand,
            "color" : soup.select(".product-stage__color")[0].get_text(),
            "price" : to_number(soup.select(PRICE_PAGE_SELECTOR[0].get_text())),
            "title" : title.strip()
        })

    def _scrape_paged(self):
        page = 1

        while True:
            url = f"{self.inp}?pagenumber={page}"

            try:
                data = self._get_overview(url)
            except ZeroItems:
                logging.debug("No more pages, finishing up")
                break

            yield ScrapeResults(url, data)

            page += 1
            logging.debug(f"Setting next url: {url}")