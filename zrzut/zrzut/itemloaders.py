from itemloaders.processors import TakeFirst, MapCompose, ChainMap
from scrapy.loader import ItemLoader

from zrzut.utils import NUMBERS_PATTERN

u_to_pln = lambda z: int(NUMBERS_PATTERN.search(z).group())

class ZrzutaLoader(ItemLoader):

    default_output_processor = TakeFirst()
    zebrano_in = MapCompose(u_to_pln)
    cel_in = MapCompose(u_to_pln)
