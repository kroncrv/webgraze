from webgraze.scraper import Scraper, ScrapeResults
from webgraze.utils import ZeroItems, to_number
import json
import logging

class ZalandoScraper(Scraper):
    DOMAIN = "zalando.(de|nl)"
    NAME = "zalando"

    def _get_soup(self, url, selector):
        soup = super()._get_soup(url, headers = {
            "user-agent" : "Mozilla/5.0"
        })

        script = soup.select(selector)[0].get_text()
        script = script.replace("]]>", "").replace("<![CDATA[", "")

        return json.loads(script)

    def _transform(self, item):
        return {
            "sku" : item["sku"],
            "name" : item["name"],
            "price_original" : self._get_price(item["price"]["original"]),
            "price_promo" : self._get_price(item["price"]["promotional"]),
            "brand_name" : item["brand_name"],
            "is_premium" : item["is_premium"],
            "product_group" : item["product_group"]
        }

    def _scrape_item(self):
        data = self._get_soup(self.inp, "#z-vegas-pdp-props")

        yield ScrapeResults(self.inp, data)

    def _scrape_paged(self):
        url = self.inp
        logging.debug(f"Starting with < {url} >")

        while True:
            data = self._get_soup(url, "#z-nvg-cognac-props")

            yield ScrapeResults(url, data["articles"])

            if "next_page_path" not in data:
                logging.debug("No more pages, finishing up")
                break
            else:
                url = f"https://www.{self.domain}" + data["next_page_path"]
                logging.debug(f"Setting next url: {url}")