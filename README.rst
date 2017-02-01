.. image:: https://travis-ci.org/MacHu-GWU/crawl_trulia-project.svg?branch=master

.. image:: https://img.shields.io/pypi/v/crawl_trulia.svg

.. image:: https://img.shields.io/pypi/l/crawl_trulia.svg

.. image:: https://img.shields.io/pypi/pyversions/crawl_trulia.svg


Welcome to crawl_trulia Documentation
===============================================================================
This is a small project provide url route, html parse tools to crawl www.trulia.com.


**Quick Links**
-------------------------------------------------------------------------------
- `GitHub Homepage <https://github.com/MacHu-GWU/crawl_trulia-project>`_
- `PyPI download <https://pypi.python.org/pypi/crawl_trulia>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/crawl_trulia-project/issues>`_


**Usage**
-------------------------------------------------------------------------------
A real example:

.. code-block:: python

    >>> from crawl_trulia.urlencoder import urlencoder
    >>> from crawl_trulia.htmlparser import htmlparser
    >>> from crawlib.spider import spider # install crawlib first

    # use address, city and zipcode
    >>> address = "22 Yew Rd"
    >>> city = "Baltimore"
    >>> zipcode = "21221"

    >>> url = urlencoder.by_address_city_and_zipcode(address, city, zipcode)
    >>> html = spider.get_html(url)
    >>> house_detail_data = htmlparser.get_house_detail(html)
    >>> house_detail_data
    {
        "features": {}, 
        "public_records": {
            "AC": "a/c", 
            "basement_type": "improved basement (finished)", 
            "bathroom": 2, 
            "build_year": 1986, 
            "county": "baltimore county", 
            "exterior_walls": "siding (alum/vinyl)", 
            "heating": "heat pump", 
            "lot_size": 7505, 
            "lot_size_unit": "sqft", 
            "partial_bathroom": 1, 
            "roof": "composition shingle", 
            "sqft": 998
        }
    }

    # usually combination of address and zipcode is enough
    >>> address = "2004 Birch Rd"
    >>> zipcode = "21221"

    >>> url = urlencoder.by_address_and_zipcode(address, zipcode)
    >>> html = spider.get_html(url)
    >>> house_detail_data = htmlparser.get_house_detail(html)

    
.. _install:

Install
-------------------------------------------------------------------------------

``crawl_trulia`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install crawl_trulia

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade crawl_trulia