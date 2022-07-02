# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import logging
import os
import re

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline, ImageException
from itemadapter import ItemAdapter

# from zrzut.utils import NUMBERS_PATTERN
NUMBERS_PATTERN = re.compile(r"\d+")
PLACEHOLDR_IMG_PATTERN = re.compile(r"zrzutka.pl/assets/imgs/cover")

logger = logging.getLogger(__name__)
u_to_pln = lambda z: int(NUMBERS_PATTERN.search(z).group())

class ZrzutPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('zebrano'):
            adapter['zebrano'] = u_to_pln(adapter['zebrano'])
        else:
            raise DropItem(f"Missing 'zebrano' in {item}")
        if adapter.get('cel'):
            adapter['cel'] = u_to_pln(adapter['cel'])
        
        return item

class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item

class ZrzutImagesPipeline(ImagesPipeline):
    
    def get_images(self, response, request: Request, info, *, item=None):
        adapter = ItemAdapter(item)
        logger.info(f"item:{item}")
        if PLACEHOLDR_IMG_PATTERN.search(adapter['img_url'][0]):
            raise ImageException("skipping zrzutka's placeholder image!")
        else:
            return super().get_images(response, request, info, item=item)

    def get_media_requests(self, item, info):
        yield Request(ItemAdapter(item)['img_url'])

    def file_path(self, request, response=None, info=None, *, item=None):
        return ItemAdapter(item)['id'] + os.path.splitext(request.url)[-1]