from webgraze.scraper import Scraper, ScrapeResults

class ExampleScraper(Scraper):
    DOMAIN = "example.com"
    NAME = "example"

    def _scrape_item(self):
        soup = self._get_soup(self.inp)

        yield ScrapeResults(self.inp, {
            "title" : soup.select("title")[0].get_text(),
            "header" : soup.select("h1")[0].get_text(),
            "charset" : soup.select("meta[charset]")[0].get("charset")
        })