"""
author:liuyongqian
date: 2020-12-20
"""
from ..forms import BaseForm
from wtforms import StringField,IntegerField,Form
from wtforms.validators import Regexp,Email,InputRequired,ValidationError,EqualTo,Length
from utils import zlcache

# 登录表单验证

class SignupForm(BaseForm):
        telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
        email = StringField(validators=[Email()])
        username = StringField(validators=[Length(3, 20)])
        password1 = StringField(validators=[Length(6, 20)])
        password2 = StringField(validators=[EqualTo("password1")])

class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    remeber = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])