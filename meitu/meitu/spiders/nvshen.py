import scrapy
import re
from pathlib import Path
from playwright.async_api import async_playwright
import datetime
import pandas as pd

# proxy_pool
from meitu.settings import ipPool
import requests

from meitu.settings import DEFAULT_REQUEST_HEADERS


class NvshenSpider(scrapy.Spider):
    name = 'nvshen'
    allowed_domains = []
    start_urls = ['https://www.meitu131.com/nvshen/']

    # proxy_pool
    for i in requests.get('http://localhost:5010/all/?type=http').json():
        ipPool.append('http://' + i['proxy'])

    # prepare for csv file
    Path('./rst').mkdir(exist_ok=True)
    df = pd.DataFrame(columns=['Score', 'Quantity', 'ID', 'Name', 'Location', 'Occupation', 'Age', 'Birthday', 'Height', 'Weight', 'B-W-H', 'Introduction'])

    def parse(self, response, **kwargs):
        pul = []
        a = response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()
        b = re.sub('([^0-9])', '', a)
        mpn = int(b)
        # mpn = int(re.sub('([^0-9])', '', response.xpath('//*[@id="pages"]/a[text()="尾页"]/@href').extract_first()))
        for i in range(1, mpn + 1):
            pul.append('index.html' if i == 1 else 'index_' + str(i) + '.html')
        yield from response.follow_all(urls=pul, callback=self.parse_m, headers=DEFAULT_REQUEST_HEADERS)

    def parse_m(self, response):
        midl = []
        for i in response.xpath('/html/body/div[1]/div[2]/ul/li/div[2]/p[1]/a/@href').extract():
            midl.append(re.sub('([^0-9])', '', i))
        mul = []
        for j in range(1, int(max(midl)) + 1):
            mul.append(str(j))
        yield from response.follow_all(urls=mul, callback=self.parse_i, headers=DEFAULT_REQUEST_HEADERS)

    async def parse_i(self, response):

        # activate playwright in async mode
        async with async_playwright() as p:
            b = await p.webkit.launch(headless=True)  # open browser in headless mode
            t = await b.new_page()  # open new tab
            await t.goto(response.url)
            s = await t.inner_text('//*[@id="diggnum"]')  # Score
            await b.close()
        q = re.sub('([^0-9])', '', response.xpath('/html/body/div[3]/div[1]/span/text()').extract_first())  # Quantity
        mid = re.sub('([^0-9])', '', response.url[response.url.find('nvshen'):])  # ID
        n = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[2]/h3/text()').extract_first()  # Name
        l, sep, o = response.xpath('//*[@id="meinv-wrapper"]/div[1]/div/div[3]/span/text()').extract_first().partition(' / ')  # Location, Occupation
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
            db['B-W-H'] = db['B-W-H'].str.replace(' ', '-').str.replace('B', '').str.replace('W', '').str.replace('H', '')
            db.to_csv('./rst/nvshen_dl.csv', index=False)
