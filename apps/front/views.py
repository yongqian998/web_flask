"""
author:liuyongqian
date: 2020-12-20
"""
from flask import (Blueprint,
                   views,
                   render_template,
                   make_response,
                    abort,
                   request,session,
                   url_for,
                   g)
import config
from .forms import SignupForm,SigninForm,AddPostForm,AddCommentForm
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightPostModel
from .models import FrontUser
from utils import restful,zlcache
from utils.captcha import Captcha
from io import BytesIO
from .models import FrontUser
from exts import db,mail
from .decorators import login_required
from flask_mail import Message
import random
import string
import json
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.sql import func

bp=Blueprint("front",__name__)


@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    sort = request.args.get("st",type=int,default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    pasts = None
    total = 0

    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html',**context)

@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html',post=post)

@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form=AddCommentForm(request.form)
    if form.validate():
        content= form.content.data
        post_id = form.post_id.data
        post=PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post=post
            comment.author=g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())


@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')
            post = PostModel(title=title,content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


#邮件发送
@bp.route('/email_captcha/')
def email_captcha():
    email=request.args.get('email')
    if not email:
        return restful.params_error("请传递邮箱参数！")
    #获取随机的验证码
    source=list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha="".join(random.sample(source,6))
    #给这个邮箱发送验证码
    message = Message("刘永倩后台管理系统邮件发送",
                      recipients=[email],
                      body="您的验证码是：%s"%captcha)
    #异常处理和捕获
    try:
        mail.send(message)
    except:
        return restful.server_error()
    # zlcache.set(email,captcha)
    return restful.success()

# @bp.route('/signup/')
# def signup():
#     return render_template('front/front_signup.html')
#
# @bp.route('/asignup/',methods=['POST'])
# def asignup():
#     form=SignupForm(request.form)
#     if form.validate():
#         telephone = form.telephone.data
#         username = form.username.data
#         password = form.password1.data
#         user = FrontUser(telephone=telephone, username=username, password=password)
#         db.session.add(user)
#         db.session.commit()


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')
    def post(self):
        form=SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username=form.username.data
            password=form.password1.data
            email=form.email.data
            user = FrontUser(telephone=telephone,username=username,password=password,email=email)
            db.session.add(user)
            db.session.commit()
            return render_template('front/front_signin.html')
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))

class SigninView(views.MethodView):
    def get(self):
        # return_to = request.referrer
        # if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(return_to):
        #     return render_template('front/front_signin.html',return_to=return_to)
        # else:
            return render_template('front/front_signin.html')
    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember=form.remeber.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())

bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))