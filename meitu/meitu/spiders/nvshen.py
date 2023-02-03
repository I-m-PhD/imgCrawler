import scrapy
import re
from pathlib import Path
from playwright.async_api import async_playwright
import datetime
import pandas as pd
import requests


class NvshenSpider(scrapy.Spider):
    name = 'nvshen'
    allowed_domains = []
    start_urls = ['https://www.meitu131.net/nvshen/']

    # prepare proxy
    @staticmethod
    def get_proxy():
        return requests.get(url='http://127.0.0.1:5010/get/').json()

    @staticmethod
    def del_proxy(proxy):
        requests.get(url='http://127.0.0.1:5010/delete/?proxy={}'.format(proxy))

    # prepare for csv file
    Path('./rst').mkdir(exist_ok=True)
    df = pd.DataFrame(
        columns=['Score', 'Quantity', 'ID', 'Name', 'Location', 'Occupation', 'Age', 'Birthday', 'Height', 'Weight',
                 'B-W-H', 'Introduction'])

    def parse(self, response, **kwargs):
        pul = []
        mpn = int(re.sub(pattern='([^0-9])', repl='',
                         string=response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()))
        for i in range(1, mpn + 1):
            pul.append('index.html' if i == 1 else 'index_' + str(i) + '.html')
        # use proxy
        retry_count = 5
        proxy = self.get_proxy().get('proxy')
        while retry_count > 0:
            try:
                yield from response.follow_all(urls=pul, callback=self.parse_m,
                                               meta={'proxy': 'http://{}'.format(proxy)})
            except Exception:
                retry_count -= 1
        self.del_proxy(proxy)

    def parse_m(self, response):
        midl = []
        for i in response.xpath('/html/body/div[1]/div[2]/ul/li/div[2]/p[1]/a/@href').extract():
            midl.append(re.sub(pattern='([^0-9])', repl='', string=i))
        mul = []
        for j in range(1, int(max(midl)) + 1):
            mul.append(str(j))
        # use proxy
        retry_count_m = 5
        proxy = self.get_proxy().get('proxy')
        while retry_count_m > 0:
            try:
                yield from response.follow_all(urls=mul, callback=self.parse_i,
                                               meta={'proxy': 'http://{}'.format(proxy)})
            except Exception:
                retry_count_m -= 1
        self.del_proxy(proxy)

    async def parse_i(self, response):
        # activate playwright in async mode
        async with async_playwright() as p:
            b = await p.webkit.launch(headless=True)  # open browser in headless mode
            t = await b.new_page()  # open new tab
            await t.goto(response.url)
            s = await t.inner_text('//*[@id="diggnum"]')  # Score
            await b.close()
        q = re.sub(pattern='([^0-9])', repl='',
                   string=response.xpath('/html/body/div[3]/div[1]/span/text()').extract_first())  # Quantity
        mid = re.sub(pattern='([^0-9])', repl='', string=response.url[response.url.find('nvshen'):])  # ID
        n = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[2]/h3/text()').extract_first()  # Name
        l, sep, o = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[3]/span/text()').extract_first().partition(
            ' / ')  # Location, Occupation
        b = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[4]/div[1]/span/text()').extract_first()  # Birthday
        age = datetime.date.today().year - int(b[:4])  # Age
        h = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[4]/div[2]/span/text()').extract_first()  # Height
        w = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[4]/div[3]/span/text()').extract_first()  # Weight
        bwh = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[4]/div[4]/span/text()').extract_first()  # B-W-H
        i = response.xpath('//*[@id="meinv-wrapper"]/div[2]/text()').extract_first().strip()  # Introduction
        # save into csv file
        self.df.loc[len(self.df)] = [s, q, mid, n, l, o, age, b, h, w, bwh, i]
        self.df.to_csv('./rst/nvshen.csv', index=False)
        # sort and clean csv file
        if Path('./rst/nvshen.csv').exists():
            db = pd.read_csv('./rst/nvshen.csv').sort_values(by=['Score'], ascending=False)
            db['B-W-H'] = db['B-W-H'].str.replace(' ', '-').str.replace('B', '').str.replace('W', '').str.replace('H',
                                                                                                                  '')
            db.to_csv('./rst/nvshen_dl.csv', index=False)
