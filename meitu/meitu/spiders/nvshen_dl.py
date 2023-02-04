import scrapy
import pandas as pd
from pathlib import Path
import re
from meitu.items import MeituItem


class NvshenDlSpider(scrapy.Spider):
    name = 'nvshen_dl'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/nvshen/']

    def parse(self, response, **kwargs):
        dl = pd.read_csv('./rst/nvshen_dl.csv') if Path('./rst/nvshen_dl.csv').exists() else print('\n', '!'*18, ' CSV FILE NOT FOUND ', '!'*18, '\n')

        """
        For how many girls you want to collect
        change the duration as you wish (make sure y > x)
        refer to the line numbers in nvshen_dl.csv 
        "x=0, y=1" will get you images of the model in line 2
        "x=166, y=167" will get you images of the model in line 168 (i.e. 肉肉)
        """
        x = 166
        y = 167
        for i in range(x, y):
            n = dl.iloc[i]['Name']
            mu = dl.iloc[i]['ID']
            yield response.follow(url=str(mu), callback=self.parse_m, meta={'n': n})

    def parse_m(self, response):
        n = response.meta['n']
        for i in response.xpath('/html/body/div[3]/div[2]/ul/li/div[2]/a'):
            au = i.xpath('@href').extract_first()
            at = re.sub('([^0-9\u4e00-\u9fff\u0041-\u005a\u0061-\u007a])', '', i.xpath('text()').extract_first())
            yield response.follow(url=au, callback=self.parse_a, meta={'n': n, 'at': at})

    def parse_a(self, response):
        n = response.meta['n']
        at = response.meta['at']
        mpu = response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()
        mpn = int(mpu[mpu.find('_')+1:mpu.find('.html')])
        ipul = []
        for i in range(1, mpn+1):
            ipul.append('index.html' if i == 1 else 'index_'+str(i)+'.html')
        yield from response.follow_all(urls=ipul, callback=self.parse_i, meta={'n': n, 'at': at})

    @staticmethod
    def parse_i(response):
        item = MeituItem()
        item['name'] = response.meta['n']
        item['album_title'] = response.meta['at']
        item['img_url'] = response.xpath('//*[@id="main-wrapper"]/div[2]/p/a/img/@src').extract_first()
        yield item
