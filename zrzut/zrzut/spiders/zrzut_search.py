import scrapy
from scrapy.exceptions import UsageError

from zrzut.utils import SORT_OPTIONS, NUMBERS_PATTERN
from zrzut.items import Zrzuta

PAGE_SUFFIX = "&page={}"

class ZrzutSearchSpider(scrapy.Spider):
    name = 'zrzut_search'
    allowed_domains = ['zrzutka.pl']
    # INTERESTING: zrzutka changed this url on 29th June
    # base_url = 'https://zrzutka.pl/katalog/list?types[0]=all'
    base_url = 'https://zrzutka.pl/catalog/list?types[0]=all'
    
    custom_settings = {
        'IMAGES_URLS_FIELD' : 'img_url'
    }

    def __init__(self, sort=None, start_page = '0', max_pages=-1, name=None, **kwargs) -> None:
        """

        Args:
            sort (str, optional): sort mode. Defaults to None, which returns the same results as `popular`, the default sort for zrzutka.
            start_page (str, optional): Start page. Defaults to '0'.
            max_pages (int, optional): How many pages should be scraped at most. Defaults to -1, which never stops, but is not asynchronous.

        Raises:
            KeyError: on invalid query arguments.
        """
        super().__init__(name, **kwargs)
        self.qs = ['']
        # args:
        if sort is not None:
            if sort not in SORT_OPTIONS:
                raise UsageError(f"argument `sort` must be one of {SORT_OPTIONS}")
            self.qs.append(f"sort={sort}")
        if max_pages != -1:
            self.max_pages = int(max_pages)
        self.start_page = int(start_page)
        self.base_url = self.base_url + '&'.join(self.qs) 

    def start_requests(self):
        if self.max_pages < 0:
            url = self.base_url + PAGE_SUFFIX.format(self.start_page)
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
            try:
                z['title'] = div.css('h5::text').get().strip()
            except AttributeError:
                z['title'] = "NA"
            zebrano = div.css('span[class="h5 mb-2"]::text').get()
            if zebrano is None:
                zebrano = div.css('div[class="h5 m-0"]::text').get()
                if zebrano is None:
                    zebrano = div.css('h5[class="m-0"]::text').get()
            try:
                z['zebrano'] = zebrano.strip()
            except AttributeError:
                z['zebrano'] = "NA"
            
            # TODO: parse cel
           
            z['img_url'] = div.css('img::attr(src)').get()
            yield z
        
        if self.max_pages < 0:
            # synchronous
            page_no = int(NUMBERS_PATTERN.search(response.url[response.url.find('page='):]).group())
            yield response.follow(self.base_url+PAGE_SUFFIX.format(page_no+1))
