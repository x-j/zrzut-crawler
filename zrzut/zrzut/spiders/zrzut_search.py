import re
import scrapy

from zrzut.utils import SORT_OPTIONS
from zrzut.items import Zrzuta

NUMBERS_PATTERN = re.compile(r"\d+")
PAGE_SUFFIX = "&page={}"

class ZrzutSearchSpider(scrapy.Spider):
    name = 'zrzut_search'
    allowed_domains = ['zrzutka.pl']
    base_url = 'https://zrzutka.pl/katalog/list?types[0]=all'
    
    def __init__(self, sort=None, name=None, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.qs = ['']
        # args:
        if sort is not None:
            if sort not in SORT_OPTIONS:
                raise KeyError(f"argument `sort` must be one of {SORT_OPTIONS}")
            self.qs.append(sort)
        
        self.base_url = self.base_url + '&'.join(self.qs) 
        self.start_urls = [self.base_url + PAGE_SUFFIX.format(0)]

    def parse(self, response):
        page_no = int(NUMBERS_PATTERN.search(response.url[response.url.find('page='):]).group())
        for div in response.xpath('/html/body/div[@class="col-sm-6 col-xl-4 pb-4"]'):
            zurl = (div.css('a::attr(href)').get())
            if zurl is None: continue
            zurl = zurl.strip()
            if zurl == '#': continue
            zid = (div.css('a::attr(data-id)').get())
            zebrano = div.css('span[class="h5 mb-2"]::text').get()
            if zebrano is None:
                try:
                    zebrano = (div.css('div[class="h5 m-0"]::text').get().strip())
                except AttributeError:
                    zebrano = (div.css('h5[class="m-0"]::text').get().strip())
            else:
                zebrano = zebrano.strip()
            yield Zrzuta(
                url = zurl, id = zid, title = div.css('h5::text').get().strip(),
                img_url = div.css('img::attr(src)').get(),
                zebrano = zebrano)
        yield response.follow(self.base_url+PAGE_SUFFIX.format(page_no+1))
