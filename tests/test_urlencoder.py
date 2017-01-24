#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import webbrowser
from crawl_trulia.urlencoder import urlencoder

todo = [
    # raw address, formatted address, zipcode
    ("2818 w shady shores rd", "2818 W Shady Shores Rd", 76208),
]


class TestUrlEncoder:

    def test_format_address(self):
        for address, formatted, zipcode in todo:
            assert urlencoder.format_address(address) == formatted

    def test_by_address_and_zipcode(self):
        for address, formatted, zipcode in todo:
            query_url = urlencoder.by_address_and_zipcode(address, zipcode)
            webbrowser.open(query_url)

if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
