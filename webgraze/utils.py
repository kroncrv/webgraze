from dataknead import Knead
from pathlib import Path
from urllib.parse import urlparse
import logging

def combine(in_path, out_path):
    if not out_path:
        raise Exception("Need an output path for combining")

    if not Path(in_path).is_dir():
        raise Exception(f"Trying to merge json files, but input is a dir: {in_path}")

    blobs = []

    logging.debug(f"Merging json files from <{in_path}>")

    files = list(Path(in_path).glob("*.json"))

    if len(files) == 0:
        raise Exception(f"No json files found in <{in_path}>")

    for path in files:
        logging.debug(f"Merging items from <{path}>")

        data = Knead(str(path)).data()["data"]

        blobs += data

    Knead(blobs).write(out_path)

def get_domain_from_url(url):
    uri = urlparse(url)
    print(uri)
    domain = ".".join(uri.netloc.split(".")[-2:])
    return domain

def iter_path(path, pattern = "*"):
    if Path(path).is_file():
        yield str(path)
    else:
        for filepath in Path(path).glob(pattern):
            yield str(filepath)

def reparse(in_path, output = None, pretty = False, overwrite = False, paged = False):
    from .scrapergetter import get_scraper_by_name

    for path in iter_path(in_path, pattern = "*.json"):
        logging.info(f"Reparsing <{path}>")
        data = Knead(path).data()
        Scraper = get_scraper_by_name(data["meta"]["scraper"])
        logging.debug(f"Found scraper <{Scraper.NAME}>")

        scraper = Scraper(data,
            reparse = True,
            paged = paged
        )

        if overwrite:
            logging.info(f"Overwriting file: <{path}>")
            output = path

        scraper.scrape(output = output, pretty = pretty)

def to_number(number):
    # This could probably be done easier, but i'm lazy
    s = ""

    for char in number:
        if char == "," or char == "." or char.isdigit():
            s += char

    s = s.replace(",", ".")

    return s

class ZeroItems(BaseException):
    pass