# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class MeituPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(url=item['img_url'], meta={'name': item['name'], 'album_title': item['album_title']})

    def file_path(self, request, response=None, info=None, *, item=None):
        fn = r'rst/%s/%s/%s' % (request.meta['name'], request.meta['album_title'], request.url[-10:])
        return fn
