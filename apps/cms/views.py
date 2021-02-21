"""
author:liuyongqian
date: 2020-12-20
"""
from flask import (Blueprint,
                   views,g,
                   render_template,
                   request,session,
                   redirect,url_for,
                   jsonify,)
from .forms import (LoginForm,
                    ResetpwdForm,
                    AddBannerForm,
                    UpdateBannerForm,
                    AddBoardForm,
                    ResetEmailForm,
                    UpdateBoardForm,
                    )
from .models import CMSUser,CMSPersmission
from .decorators import login_required,permission_required
import config
from exts import db,mail
from utils import restful,zlcache
from flask_mail import Message
import string
import random
from ..models import BannerModel,BoardModel,PostModel,HighlightPostModel
bp=Blueprint("cms",__name__,url_prefix="/cms")


#这是访问首页
@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')
#这是注销功能
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))
#访问个人中心页面
@bp.route('/profile')
@login_required
def profile():
    return render_template('cms/cms_profile.html')
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
    zlcache.set(email,captcha)
    return restful.success()
#
# @bp.route('/email/')
# def send_email():
#     message=Message("刘永倩后台管理系统邮件发送",
#                     recipients=['3092806186@qq.com'],
#                     body="你好 我是邮件发送者")
#     mail.send(message)
#     return 'succes'


@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    post_list = PostModel.query.all()
    return render_template('cms/cms_posts.html',posts=post_list)


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()
@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html',**context)

@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error('请传入板块id！')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()

@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')

@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)

@bp.route('/abanner/',methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())
@bp.route('/dbanner/',methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()

class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template("cms/cms_login.html",message=message)
    def post(self):
        form=LoginForm(request.form)
        if form.validate():

            email=form.email.data
            password=form.password.data
            remember=form.remenber.data

            user = CMSUser.query.filter_by(email=email).first()


            #验证密码
            if user and user.check_password(password):
                session[config.CMS_USER_ID]=user.id

                if remember:
                    #session.permanent=True默认31天过期
                    session.permanent=True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="邮箱或密码错误！")

        else:
            #取第一个的message  form.errors--》返回一个字典
            #popitem()---》返回任意元素
            message=form.get_error()
            return self.get(message=message)

class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # {"code":200,message=""}
                # return jsonify({"code":200,"message":""})
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_error())

class ResetEmailView(views.MethodView):
    decorators=[login_required]
    def get(self):
        return render_template("cms/cms_resetemail.html")
    def post(self):
        form =ResetEmailForm(request.form)
        if form.validate():
            email=form.email.data
            g.cms_user.email=email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))