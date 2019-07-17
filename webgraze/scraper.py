from bs4 import BeautifulSoup
from dataknead import Knead
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from .utils import get_domain_from_url, to_number
import html
import json
import logging
import requests
import re

DEFAULT_INDENT = 4

class ScrapeResults:
    def __init__(self, url, data, output_filename = None):
        self.url = url
        self.data = data
        self.output_filename = output_filename

class Scraper:
    def __init__(self, inp,
        paged = False,
        input_file = False,
        page_suffix = None,
        reparse = False,
        overwrite = False
    ):
        self.last_html = None # FIXME: this is a hack
        self.output = None # FIXME: this is a hack
        self.reparse = reparse
        self.inp = inp
        self.paged = paged
        self.overwrite = overwrite

        if not self.reparse:
            self.domain = get_domain_from_url(inp)

        self.input_file = input_file

        if page_suffix:
            self.page_suffix = f"{page_suffix}-"
        else:
            self.page_suffix = ""

    def _get_soup(self, inp, headers = {}):
        if self.reparse:
            return BeautifulSoup(inp["html"], features = "lxml")

        if self.input_file:
            logging.debug(f"Getting a file")
            with open(inp) as f:
                html = f.read()
        else:
            logging.info(f"Requesting URL <{inp}>")
            req = requests.get(inp, headers = headers)
            logging.debug(f"Got <{inp}>")
            html = req.text

        soup = BeautifulSoup(html, features = "lxml")

        self.last_html = str(soup)

        return soup

    def _scrape_item(self):
        raise NotImplementedError

    def _scrape_paged(self):
        raise NotImplementedError

    def _add_metadata(self, data):
        # FIXME: this feels a bit wonky
        if self.reparse:
            self.inp["data"] = data.data
            return self.inp

        return {
            "data" : data.data,
            "html" : self.last_html,
            "meta" : {
                "domain" : self.domain,
                "scrape_time" : datetime.now().isoformat("T"),
                "scrape_url" : data.url,
                "scraper" : self.NAME
            }
        }

    def _scrape(self):
        if self.paged:
            return self._scrape_paged()
        else:
            return self._scrape_item()

    def _save(self, results, output = None, pretty = None):
        item = self._add_metadata(results)

        if pretty:
            indent = DEFAULT_INDENT
        else:
            indent = None

        if output:
            logging.debug(f"Saving to <{output}>")

            # Does path exists, and if so, raise exception
            if Path(output).exists() and not self.overwrite:
                raise Exception(f"Path exists <{output}>")

            Knead(item).write(output, indent = indent)
        else:
            print(json.dumps(item["data"], indent = indent))

    def scrape(self, output = None, pretty = None):
        logging.debug(f"Scraping to {output}, pretty? {pretty}")

        # FIXME: this feels wonky
        if self.reparse:
            results = next(self._scrape())
            self._save(results, output, pretty = pretty)
            return

        if self.paged and not output:
            raise Exception("Paged scraping needs an output")

        if self.paged and not Path(output).is_dir():
            logging.debug(f"Creating directory {output}")
            Path(output).mkdir(parents = True, exist_ok = False)

        self.output = output

        for (index, item) in enumerate(self._scrape()):
            index = index + 1

            if not isinstance(item, ScrapeResults):
                raise Exception("Scrape results are the incorrect type")

            if output and self.paged:
                # Check for a special filename, otherwise just use default
                if item.output_filename:
                    out_filepath = f"{output}/{item.output_filename}"
                else:
                    out_filepath = f"{output}/page-{self.page_suffix}{index}.json"
            else:
                out_filepath = output

            self._save(item, out_filepath, pretty = pretty)