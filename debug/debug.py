#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dataIO import js, textfile
from crawl_trulia import trulia_urlencoder, trulia_htmlparser
from crawl_trulia.packages.crawlib.spider import spider

PATH = "test.html"

address = "22 Yew Rd"
city = "Baltimore"
zipcode = "21221"

# url = urlencoder.by_address_and_zipcode(address, zipcode)
url = trulia_urlencoder.by_address_city_and_zipcode(address, city, zipcode)

if not os.path.exists(PATH):
    html = spider.get_html(url, encoding="utf-8")
    textfile.write(html, PATH)

html = textfile.read(PATH)
data = trulia_htmlparser.get_house_detail(html)
js.pprint(data)