#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module is to parse html to get useful information from trulia.
"""

try:
    from .helpers import int_filter, float_filter
    from .packages.crawlib.htmlparser import BaseHtmlParser
except:
    from crawl_trulia.helpers import int_filter, float_filter
    from crawl_trulia.packages.crawlib.htmlparser import BaseHtmlParser


class HTMLParser(BaseHtmlParser):
    
    def parse_house_details(self, public_records):
        """Parse label and value of house detail from text.
        
        **中文文档**
        
        从features或public_records的字符中解析出具体信息。
        """
        results = dict()
        
        for field in public_records:
            field = field.lower()
            # 价格
            if "price" in field:
                results["price"] = int_filter(field)
            
            # 房子类别
            elif "single-family" in field:
                results["house_type"] = "single family"
            
            elif "townhouse" in field:
                results["house_type"] = "town house"
            
            elif "multi-family" == field:
                results["multi_family"] = True

            # 面积
            elif ("sqft" in field) and ("lot size" not in field):
                results["sqft"] = int_filter(field)
                
            # 院子面积
            elif ("sqft" in field) and ("lot size" in field):
                results["lot_size"] = int_filter(field)
                results["lot_size_unit"] = "sqft"
            elif ("acres" in field) and ("lot size" in field):
                results["lot_size"] = float_filter(field)
                results["lot_size_unit"] = "acer"
                
            # 卧室
            elif "bedroom" in field:
                results["bedroom"] = int_filter(field)
                
            # 洗手间
            elif ("bathroom" in field) and ("partial" not in field):
                results["bathroom"] = int_filter(field)

            # 小洗手间
            elif "partial bathroom" in field:
                results["partial_bathroom"] = int_filter(field)

            # 市场状态
            elif "status:" in field:
                results["status"] = field.split(":")[-1].strip()
                
            # 供暖方式
            elif "heating:" in field:
                results["heating"] = field.split(":")[-1].strip()
            
            # 供暖燃料
            elif "heating fuel:" in field:
                results["heating_fuel"] = field.split(":")[-1].strip()
                
            # HVAC
            elif "a/c" == field:
                results["AC"] = field.split(":")[-1].strip()
            
            #--- 设施类 ---
            # 电扇
            elif "ceiling fan" == field:
                results["ceailing_fan"] = True
            
            # 冰箱
            elif "refrigerator" == field:
                results["refrigerator"] = True
                
            # 洗衣机
            elif "washer" == field:
                results["washer"] = True
                
            # 洗碗机
            elif "dryer" == field:
                results["dryer"] = True
            
            #--- 建筑 ---
            # 地基
            elif "foundation:" in field:
                results["foundation"] = field.split(":")[-1].strip()
            
            # 地板
            elif "floors:" in field:
                results["floors"] = field.split(":")[-1].strip()
                
            # 外墙
            elif "exterior walls:" in field:
                results["exterior_walls"] = field.split(":")[-1].strip()
            
            # 房顶
            elif "roof:" in field:
                results["roof"] = field.split(":")[-1].strip()

            # 地下室
            elif "basement:" in field:
                results["basement_type"] = field.split(":")[-1].strip()
            
            elif "basement" == field:
                results["basement"] = True
            
            # 建造年份
            elif "built in" in field:
                results["build_year"] = int_filter(field)
            
            # 风格
            elif "style:" in field:
                results["style"] = field.split(":")[-1].strip()
            
            # 建造方式
            elif "construction:" in field:
                results["construction"] = field.split(":")[-1].strip()
            
            # 停车
            elif "parking:" in field:
                results["parking"] = field.split(":")[-1].strip()
                
            # 泳池
            elif "pool:" in field:
                results["pool"] = field.split(":")[-1].strip()
            
            # 邻居
            elif "Neighborhood:" in field:
                results["neighborhood"] = field.split(":")[-1].strip()
                
            # County
            elif "county:" in field:
                results["county"] = field.split(":")[-1].strip()
                      
            # Zipcode
            elif "zip:" in field:
                results["zipcode"] = field.split(":")[-1].strip()
            
        return results

    def get_house_detail(self, html):
        """Get all details in html.
        
        **中文文档**
        
        此函数只可能返回非空dict或是None。原理是从address_field
        """
        soup = self.get_soup(html)
        data = dict()
        
        # address, city, state, zipcode <--- this should always work
        try:
            address_field = list()
            h1 = soup.find("h1", class_=["h6", "mtn", "ptn"])
            for span in h1.find_all("span"):
                if span.string:
                    address_field.append(span.string.strip())
            if len(address_field) >= 4:
                data["address"] = address_field[0]
                data["city"] = address_field[1]
                data["state"] = address_field[2]
                data["zipcode"] = address_field[3]
        except Exception as e:
            data.setdefault("errors", dict())
            data["errors"]["address"] = repr(e)
        
        # price
        try:
            for span in soup.find_all("span", itemprop="price"):
                try:
                    data["price"] = int_filter(span.text)
                except:
                    pass
        except Exception as e:
            data.setdefault("errors", dict())
            data["errors"]["price"] = repr(e)
        
        # features
        try:
            features = list()
            for ul in soup.find_all("ul", class_="listInline pdpFeatureList"):
                for li in ul.find_all("li"):
                    if len(li.attrs) == 0:
                        features.append(li.text.strip())
            results = self.parse_house_details(features)
            data["features"] = results
        except Exception as e:
            data.setdefault("errors", dict())
            data["errors"]["features"] = repr(e)
        
        # public records
        try:
            public_records = list()
            for ul in soup.find_all("ul", class_ = "listInline mbn pdpFeatureList"):
                for li in ul.find_all("li"):
                    if len(li.attrs) == 0:
                        public_records.append(li.text.strip())
            results = self.parse_house_details(public_records)
            data["public_records"] = results
        except Exception as e:
            data.setdefault("errors", dict())
            data["errors"]["public_records"] = repr(e)
        
        if len(data) == 0:
            return None
        else:
            return data


htmlparser = HTMLParser()


def validate(data):
    """Valdiate the result data.
    """
    if data is None:
        return False
    
    errors = data.get("errors", dict())
    features = data.get("features", dict())
    public_records = data.get("public_records", dict())
    
    if len(features) or len(public_records):
        return True
    else:
        return False


def get_house_size_from_detail(data):
    """Find correct value of sqft from house detail data.
    """
    try:
        f_sqft = data["features"]["sqft"]
    except:
        f_sqft = None

    try:
        p_sqft = data["public_records"]["sqft"]
    except:
        p_sqft = None

    if (f_sqft is None) and p_sqft:
        return p_sqft
    elif f_sqft and (p_sqft is None):
        return f_sqft
    elif f_sqft and p_sqft:
        if f_sqft == p_sqft:
            return f_sqft
        # 如果两者差异小于20%, 并且数值都大于400
        elif (abs(f_sqft-p_sqft) * 1.0 / f_sqft) <= 0.2 and f_sqft >= 400 and p_sqft >= 400:
            return int(0.5 * (f_sqft + p_sqft))
        else:
            return None
    else:
        return None
    

def preprocess(raw_data):
    """Preprocess raw data, get following data points:
    
    - sqft:
    - bedroom:
    - bathroom:
    """
    data = {"sqft": None, "bedroom": None, "bathroom": None}
    
    # sqft
    try:
        f_sqft = raw_data["features"]["sqft"]
    except:
        f_sqft = None

    try:
        p_sqft = raw_data["public_records"]["sqft"]
    except:
        p_sqft = None

    if (f_sqft is None) and p_sqft:
        data["sqft"] = p_sqft
    elif f_sqft and (p_sqft is None):
        data["sqft"] = f_sqft
    elif f_sqft and p_sqft:
        if f_sqft == p_sqft:
            data["sqft"] = f_sqft
        # 如果两者差异小于20%, 并且数值都大于400, 则取平均
        elif (abs(f_sqft-p_sqft) * 1.0 / f_sqft) <= 0.2 and f_sqft >= 400 and p_sqft >= 400:
            data["sqft"] = int(0.5 * (f_sqft + p_sqft))
    
    # bedroom
    try:
        f_bedroom = raw_data["features"]["bedroom"]
    except:
        f_bedroom = None

    try:
        p_bedroom = raw_data["public_records"]["bedroom"]
    except:
        p_bedroom = None

    if (f_bedroom is None) and p_bedroom:
        data["bedroom"] = p_bedroom
    elif f_bedroom and (p_bedroom is None):
        data["bedroom"] = f_bedroom
    elif f_bedroom and p_bedroom:
        if f_bedroom == p_bedroom:
            data["bedroom"] = f_bedroom

    # bathroom
    try:
        f_bathroom = raw_data["features"]["bathroom"]
    except:
        f_bathroom = None

    try:
        p_bathroom = raw_data["public_records"]["bathroom"]
    except:
        p_bathroom = None

    if (f_bathroom is None) and p_bathroom:
        data["bathroom"] = p_bathroom
    elif f_bathroom and (p_bathroom is None):
        data["bathroom"] = f_bathroom
    elif f_bathroom and p_bathroom:
        if f_bathroom == p_bathroom:
            data["bathroom"] = f_bathroom
    
    return data


if __name__ == "__main__":
    from crawl_trulia.urlencoder import urlencoder
    from crawlib.spider import spider
    from dataIO import js, textfile
    
    address = "19810 Falling Spring Ct"
    zipcode = "20882"
    
    # download 
    url = urlencoder.by_address_and_zipcode(address, zipcode)
    html = spider.get_html(url, encoding="utf8")
    textfile.write(html, "page.html")
    
    # test
    html = textfile.read("page.html")
    data = htmlparser.get_house_detail(html)
    js.pprint(data)    
    js.pprint(preprocess(data))