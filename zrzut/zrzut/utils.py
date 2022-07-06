import re

# strings

ZRZUTKA_CATALOG_URL = 'https://zrzutka.pl/catalog/list?types[0]=all' 
# ^zrzutka switched to this url around 29th June, the one below is the old one
ZRZUTKA_KATALOG_URL = 'https://zrzutka.pl/katalog/list?types[0]=all'
PAGE_SUFFIX = "&page={}"


# regexii
NUMBERS_PATTERN = re.compile(r"(\d+ ?)+")


# query parameters
SORT_OPTIONS = {
    'popular',
    'most_funds',
    'least_funds',
    'newest',
    'oldest',
    'ending',
    'last_updated'
}