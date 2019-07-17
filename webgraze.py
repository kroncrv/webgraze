#!/usr/bin/env python3
from argparse import ArgumentParser
from webgraze.utils import combine, reparse
from webgraze.scrapergetter import get_scraper, get_scraper_by_name
import logging
import sys
logger = logging.getLogger(__name__)

class Webgraze:
    def __init__(self):
        self.parser = None
        self.get_parser()

    def get_parser(self):
        parser = ArgumentParser()
        parser.add_argument("input", nargs = "?", help = "URL or directory")
        parser.add_argument("-c", "--combine", action = "store_true",
            help = "Combine all JSON files in a directory"
        )
        parser.add_argument("-if", "--input-file", action = "store_true",
            help = "Input is not an URL, but a file"
        )
        parser.add_argument("-o", "--output", type = str,
            help = "Output file or directory"
        )
        parser.add_argument("-ow", "--overwrite", action = "store_true",
            help = "Overwrite existing files"
        )
        parser.add_argument("-p", "--paged", action = "store_true",
            help = "URL is pageable"
        )
        parser.add_argument("-ps", "--page-suffix", type = str,
            help = "Add a suffix to output page JSON files",
            default = None
        )
        parser.add_argument("--pretty", action = "store_true",
            help = "Output pretty indented JSON"
        )
        parser.add_argument("-rp", "--reparse", action = "store_true",
            help = "Reparse input file"
        )
        parser.add_argument("--scraper", help = "Force a scraper", type = str)
        parser.add_argument("-v", "--verbose", action = "store_true")
        self.parser = parser
        self.args = self.parser.parse_args()

    def is_verbose(self):
        return self.args.verbose == True

    def print_help(self):
        self.parser.print_help()
        sys.exit(0)

    def run(self):
        args = self.args

        if len(sys.argv) == 1 or not args.input:
            self.print_help()

        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("Debug logging is ON")
        else:
            logging.basicConfig(level=logging.INFO)

        logging.debug(args)

        if args.combine:
            logging.debug("Combining data")
            combine(args.input, args.output)
        elif args.reparse:
            reparse(args.input,
                output = args.output,
                pretty = args.pretty,
                overwrite = args.overwrite,
                paged = args.paged
            )
        else:
            logging.info(f"Trying to scrape <{args.input}>")
            logging.debug(f"Finding a scraper for <{args.input}>")

            if args.scraper:
                logging.debug(f"A scraper is being forced: {args.scraper}")
                Scraper = get_scraper_by_name(args.scraper)
            else:
                Scraper = get_scraper(args.input)

            logging.info(f"Scraping with {Scraper.NAME}")

            scraper = Scraper(args.input,
                paged = args.paged,
                input_file = args.input_file,
                page_suffix = args.page_suffix,
                overwrite = args.overwrite
            )

            scraper.scrape(output = args.output, pretty = args.pretty)

if __name__ == "__main__":
    grazer = Webgraze()

    try:
        grazer.run()
    except Exception as e:
        if grazer.is_verbose():
            raise(e)
        else:
            # NotImplementedError doesn't have a string representation
            if str(e) == "":
                sys.exit(e.__repr__())
            else:
                sys.exit(e)