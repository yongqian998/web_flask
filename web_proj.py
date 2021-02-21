"""
author:liuyongqian
date: 2020-12-20
"""
from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db,mail
from flask_wtf.csrf import CSRFProtect
from utils.captcha import Captcha
from flask_cors import CORS


csrf = CSRFProtect()

#定义一个工厂函数
def create_app():
    app=Flask(__name__)
    CORS(app, resources={"*": {"origins": "*"}})
    app.config.from_object(config)
    # 注册蓝图
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)

    db.init_app(app)
    mail.init_app(app)

    csrf.init_app(app)
    return app

Captcha.gene_graph_captcha()

if __name__=="__main__":
    app=create_app()
    app.run(port=8000)


