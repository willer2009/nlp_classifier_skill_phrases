import json

import scrapy

urls = []
def get_urls(filename, urls):
    with open(filename) as f:
        data = json.load(f)
        l = list(data)
        # print(data)
        # data = json.loads(data)
        for link in l:
            d = dict(link)
            urls.append("www.stepstone.de" + d['link'])
    return urls


