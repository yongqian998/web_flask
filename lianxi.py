"""
author:liuyongqian
date: 2021-01-07
"""
#extend的用法
# a=[1,2]
# b=[3,4]
# a.extend(b)
# print(a)

#string ascii_letters的用法
import string
ma=list(string.ascii_letters)
ba=string.ascii_letters
print(ba)
print(ma)

import random
ca=range(10)
for i in ca:
    b=str(i)

source=list(string.ascii_letters)
source.extend(map(lambda x:str(x),range(10)))
captcha=random.sample(source,30)
print("".join(captcha))
print(source)
