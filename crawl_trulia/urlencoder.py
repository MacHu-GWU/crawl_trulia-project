#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Because when you search an address on trulia, it actually encode your input and 
generate an url, and the trulia server will process this request. So this module 
is to create the request url based on your search.
"""

special_words = {
    "nw": "NW", "ne": "NE", "sw": "SW", "se": "SE",
    "crossing": "Xing",
}

class UrlEncoder(object):
    homepage = "http://www.trulia.com/"
    search_url = "https://www.trulia.com/submit_search/?display_select=for_sale&locationId=&locationType=&tst=h&ac_entered_query=&ac_index=&propertyId=&propertyIndex=&bedFilter=&bathFilter=&propertyFilter=&display=for+sale&search={0}" 
    
    def format_address(self, address):
        """Format an address into standard format.
        
        **中文文档**
        
        标准化的地址需要满足以下标准。
        
        1. 不允许有除 "#" 以外的特殊符号, 例如逗号, 分号。
        2. 单词之间空格只能有一个。
        3. 单词的第一个英文字母大写。
        """
        address = address.replace(",", " ").replace(";", " ").lower()
        chunks = [i.strip() for i in address.split(" ") if i.strip()]
        new_chunks = list()
        for word in chunks:
            if word.lower() in special_words:
                new_chunks.append(special_words[word.lower()])
                
            else:
                char_list = list()
                counter = 0
                for char in word:
                    if char.isalpha():
                        counter += 1
                        if counter <= 1:
                            char_list.append(char.upper())
                        else:
                            char_list.append(char)
                    else:
                        char_list.append(char)
                new_chunks.append("".join(char_list))
        address = " ".join(new_chunks)
        return address
        
    def is_formatted(self, address):
        """Check if an address is in standard format.
        """
        if address == self.format_address(address):
            return True
        else:
            return False
    
    def format_zipcode(self, zipcode):
        """Format a zipcode.
        """
        zipcode = str(zipcode).strip().zfill(5)
        return zipcode
    
    def url_encode_address(self, address):
        """trulia only accept #unit_number, and doesn't accept Apt keyword.
        And it replace the '#' with '%23', space char ' ' with plus sign'+'
        """
        address = self.format_address(address)
        address = address.replace(" ", "+").replace("#", "%23")
        return address
    
    def url_encode_city(self, city):
        city = self.format_address(city)
        city = city.replace(" ", "+")
        return city
    
    def format_search_string(self, address, city=None, zipcode=None):
        """Basically, combination of address and zipcode is enough. But the
        chance to match the address will be increased if with city.
        """
        search_str = self.url_encode_address(address)
        if city:
            search_str = search_str + "+" + self.url_encode_city(city)
        if zipcode:
            search_str = search_str + "+" + self.format_zipcode(zipcode)
        return search_str
    
    def by_search_str(self, search_str):
        url = self.search_url.format(search_str)
        return url
    
    def by_address_and_zipcode(self, address, zipcode):
        """Given address and zipcode, create the trulia query url.
        """
        search_str = self.format_search_string(address, None, zipcode)
        url = self.search_url.format(search_str)
        return url
    
    def by_address_city_and_zipcode(self, address, city, zipcode):
        """Given address, city and zipcode, create the trulia query url.
        """
        search_str = self.format_search_string(address, city, zipcode)
        url = self.search_url.format(search_str)
        return url
    
urlencoder = UrlEncoder()