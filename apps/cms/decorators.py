"""
author:liuyongqian
date: 2020-12-22
"""
from flask import session,redirect,url_for,g
from functools import wraps
import config
#定义登录装饰器--->登录限制
#session-->类似于字典
def login_required(func):
    #保留func本身的一些属性
    @wraps(func)
    def inner(*args,**kwargs):
        #判断是否登录
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    #外函数返回内函数
    return inner


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter