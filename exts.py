"""
author:liuyongqian
date: 2020-12-20
"""


from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# from utils.alidayu import AlidayuAPI

db = SQLAlchemy()
mail = Mail()
# alidayu = AlidayuAPI()