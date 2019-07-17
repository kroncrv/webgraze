# webgraze.py
> Command line web scraping utility
This project was originally created to scrape a couple of online clothing shops, so many of the inbuilt scrapers were designed to do that.

## Installation
To install dependencies the easiest way is to use [poetry](https://poetry.eustace.io/).

```bash
poetry install
poetry run ./webgraze.py
```

Otherwise use `pip`:

```bash
pip install dataknead beautifulsoup4 requests lxml
```

## Examples
This will print structured data from example.com as a JSON structure

    webscrape.py http://www.example.com

Save the output to a file called example.json

    webscrape.py http://www.example.com -o example.json

Scrape a Zalando t-shirt and save to test.json

    webgraze.py -o test.json https://www.zalando.nl/jcrew-perfect-fit-t-shirt-basic-jc421d00t-a11.html

Scrape all search results pages given a base URL on zalando.nl and save to a
   directory called `data` (note the --paged argument)

   webgraze.py -o zalando --paged https://www.zalando.nl/tassen-accessoires-koptelefoons/

Combine scrape results from a directory called 'zalando' and save to a single json file

    webgraze.py --combine -o zalando-headphones.json zalando

## Troubleshooting
* Before opening an issue, try running your command with the `-v` (verbose) switch, because this will give you more debug information.

## All options
You'll get this output when running `webgraze.py -h`.

```bash
usage: webgraze.py [-h] [-c] [-if] [-o OUTPUT] [-ow] [-p] [-ps PAGE_SUFFIX]
                   [--pretty] [-rp] [--scraper SCRAPER] [-v]
                   [input]

positional arguments:
  input                 URL or directory

optional arguments:
  -h, --help            show this help message and exit
  -c, --combine         Combine all JSON files in a directory
  -if, --input-file     Input is not an URL, but a file
  -o OUTPUT, --output OUTPUT
                        Output file or directory
  -ow, --overwrite      Overwrite existing files
  -p, --paged           URL is pageable
  -ps PAGE_SUFFIX, --page-suffix PAGE_SUFFIX
                        Add a suffix to output page JSON files
  --pretty              Output pretty indented JSON
  -rp, --reparse        Reparse input file
  --scraper SCRAPER     Force a scraper
  -v, --verbose

```

## License
Licensed under the [MIT license](https://opensource.org/licenses/MIT).

## Credits
Written by Hay Kranen for [Pointer](https://www.pointer.nl).