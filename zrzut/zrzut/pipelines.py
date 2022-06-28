# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from zrzut.utils import NUMBERS_PATTERN

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
