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
    
    def __init__(self, sort=None, start_page = '0', max_pages=None, name=None, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.qs = ['']
        # args:
        if sort is not None:
            if sort not in SORT_OPTIONS:
                raise KeyError(f"argument `sort` must be one of {SORT_OPTIONS}")
            self.qs.append(f"sort={sort}")
        if max_pages is not None:
            self.max_pages = int(max_pages)
        else:
            self.max_pages = -1
        self.start_page = int(start_page)
        self.base_url = self.base_url + '&'.join(self.qs) 

    def start_requests(self):
        if self.max_pages < 0:
            yield scrapy.Request(url, self.parse)
        else: 
            lim = self.max_pages + self.start_page
            for i in range(self.start_page, lim):
                url = self.base_url + PAGE_SUFFIX.format(i)
                yield scrapy.Request(url, self.parse) 

    def parse(self, response):
        for div in response.xpath('/html/body/div[@class="col-sm-6 col-xl-4 pb-4"]'):
            z = Zrzuta()
            z['url'] = (div.css('a::attr(href)').get())
            if z['url'] is None: continue
            z['url'] = z['url'].strip()
            if z['url'] == '#': continue
            z['id'] = (div.css('a::attr(data-id)').get())
            zebrano = div.css('span[class="h5 mb-2"]::text').get()
            if zebrano is None:
                zebrano = div.css('div[class="h5 m-0"]::text').get()
                if zebrano is None:
                    zebrano = div.css('h5[class="m-0"]::text').get()
            try:
                z['zebrano'] = zebrano.strip()
            except AttributeError:
                z['zebrano'] = "NA"
            try:
                z['title'] = div.css('h5::text').get().strip()
            except AttributeError:
                z['title'] = "NA"
            z['img_url'] = div.css('img::attr(src)').get()
            if z['img_url'] is None: z['img_url'] = "NA"
            yield z
        
        if self.max_pages < 0:
            # synchronous
            page_no = int(NUMBERS_PATTERN.search(response.url[response.url.find('page='):]).group())
            yield response.follow(self.base_url+PAGE_SUFFIX.format(page_no+1))
