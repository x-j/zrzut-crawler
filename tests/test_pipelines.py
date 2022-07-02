import pytest
import scrapy

from zrzut.zrzut.pipelines import ZrzutImagesPipeline
from zrzut.zrzut.items import Zrzuta

@pytest.fixture
def test_item():
    return Zrzuta() # TODO

dump_path = './tests/dumps'


class Test_ZrzutImagesPipeline():

    zzip = ZrzutImagesPipeline(dump_path)

    def test_get_images(self):
        pass # TODO

    def test_get_images_raises(self):
        templat_item = Zrzuta(
            img_url = ["https://zrzutka.pl/assets/imgs/cover.png"],
            id = "344zut", zebrano=0, url = "https://zrzutka.pl/d33zut")
        with pytest.raises(scrapy.pipelines.images.ImageException):
            self.zzip.get_images(response= None,
                request = scrapy.Request(templat_item['url']),
                info=None, item=templat_item)

