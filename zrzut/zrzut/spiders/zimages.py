from scrapy import Spider


class ZrzutImageSpider(Spider):
    name = 'zimages'
    allowed_domains = ['zrzutka.pl']
    custom_settings = {
        'ITEM_PIPELINES': {
            'zrzut.pipelines.ZrzutImagesPipeline': 200,
            # 'scrapy.pipelines.images.ImagesPipeline': 250,
            }
    }
    
    def __init__(self, f, name=None, **kwargs) -> None:
        """

        Args:
            f: csv file containing a column named `img_url` 

        Raises:
            KeyError: on invalid query arguments.
        """
        super().__init__(name, **kwargs)
        # todo: validate input file
    
    def start_requests(self):
        # todo: read input file and find image urls
        raise NotImplementedError