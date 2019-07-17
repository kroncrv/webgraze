from webgraze.scraper import Scraper, ScrapeResults
import logging

class QuotesScraper(Scraper):
    DOMAIN = "toscrape.com"
    NAME = "quotes"

    def _parse_item(self, item):
        tags = item.select(".tags .tag")

        return {
            "text" : item.select(".text")[0].get_text(),
            "author" : item.select(".author")[0].get_text(),
            "author_href" : item.select(".author")[0].parent.select("a")[0].get("href"),
            "tags" : [t.get_text() for t in tags]
        }

    def _parse_page(self, url):
        soup = self._get_soup(url)
        quotes = soup.select(".quote")
        next_button = soup.select(".next a")

        if next_button:
            next_href = "http://quotes.toscrape.com" + next_button[0].get("href")
        else:
            next_href = None

        return [self._parse_item(quote) for quote in quotes], next_href

    def _scrape_item(self):
        page = self._parse_page(self.inp)
        yield ScrapeResults(self.inp, page)

    def _scrape_paged(self):
        url = self.inp
        index = 1

        while True:
            page, next_url = self._parse_page(url)
            yield ScrapeResults(url, page)

            if not next_url:
                logging.debug("No more pages, finishing up")
                break
            else:
                url = next_url
                index = index + 1