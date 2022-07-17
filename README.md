# zrzut-crawler
Scrapy project for crawling through zrzutka.pl

## Usage

Basic knowledge about scrapy spiders may be necessary to run this. 

To run a spider, move to the `zrzut` directory and run the command :

`scrapy crawl zsearch`

By default, without providing any arguments, zsearch will start crawling through all pages of zrzutka.pl in a synchrounous manner.

### Spider arguments

- `sort` - sort mode to use. The default is 'most_popular'.
- `max_pages` - how many pages to crawl through at most. Every page yields 11 zrzutas, on average.
- `start_page` - page from which to start crawling.
