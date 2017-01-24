#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
import webbrowser
from pprint import pprint as ppt
from crawl_trulia.urlencoder import urlencoder
from crawl_trulia.htmlparser import htmlparser
from dataIO import js, textfile
from crawlib.spider import spider


def get_testdata():
    """

    **中文文档**

    下载测试数据
    """
    try:
        os.mkdir("testdata")
    except:
        pass

    todo = [
        ("7436 Arrowood Rd", "20817"),
        ("1860 Royal Oak St", "78520"),
        ("824 S Ridgeley Dr", "90036"),
        ("24 Franklin Ct", "06470"),
        ("5403 S Dorchester Ave", "60615"),
        ("14226 Duncannon Dr", "77015"),
        ("13915 Marble Creek Ct", "77077"),
    ]
    counter = 0
    for address, zipcode in todo:
        counter += 1
        filename = os.path.join(
            "testdata", "%s.html" % address.replace(" ", "-"))
        if not os.path.exists(filename):
            url = urlencoder.by_address_and_zipcode(address, zipcode)
            html = spider.html_with_encoding(url=url)
            textfile.write(html, filename)

get_testdata()


class TestHTMLParser:

    def test_all(self):
        for i, fname in enumerate(os.listdir("testdata")):
            path = os.path.join("testdata", fname)
            html = textfile.read(path)
            data = htmlparser.get_house_detail(html)
            print("{:=^100}".format(str(i+1).zfill(2)))
            js.pprint(data)


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
