import re

# regexii
NUMBERS_PATTERN = re.compile(r"\d+")

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