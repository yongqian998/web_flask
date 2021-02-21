"""
author:liuyongqian
date: 2020-12-22
"""
import requests
from pyquery import PyQuery as pq

result_text = requests.get("http://www.baidu.com").text
pq_html = pq(result_text)
img_item = pq_html("img").items()
for item in img_item:
    print(item.attr.src)
