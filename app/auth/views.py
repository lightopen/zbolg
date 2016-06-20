# coding=utf-8
from ..email import send_mail
from ..models import *
from .. import bootstrap
from . import auth
from .forms import *
from flask import flash, render_template, redirect, url_for, request
from flask.ext.login import login_user, logout_user, login_required, current_user

# 注册用户，并发送确认邮件，注册成功后自动登录并返回首页，待确认后用户属性改为已确认
@auth.route('/signup', methods=['GET','POST'])
def signup():
    title="注册"
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user is not None or email is not None:
            flash('Account exists, you can not signup!')
            return redirect(url_for('auth.signup'))
        user = User(
                    username = form.username.data,
                    email = form.email.data,
                    password = form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirmation', 'email_confirm', token=token)
        flash('Register success')
        flash("Please check your email, and confirm your accout")
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/form_template.html', form=form, title=title)

# 登录视图， 验证用户邮箱及密码，重定向至首页
@auth.route("/signin", methods=['GET','POST'])
def signin():
    title = "登录"
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data == user.email and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Login successful')
            return redirect(request.args.get('next', url_for('main.index')))
        flash('Login fail')
    return render_template('auth/form_template.html', form=form, title=title)

# 退出登录，登录状态下可用
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 忘记密码，通过邮箱确认，确认网址包含用户名和令牌
@auth.route('/forgetpassword', methods=['GET','POST'])
def forget_password():
    title = "忘记密码"
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_confirmation_token()
            send_mail(user.email, 'Reset password', 'auth/reset_confirm', username=user.username, token=token)
            flash("email has sent, check your email account")
            return redirect(url_for('main.index'))
        flash("Your email don't exist.Would you like register?")
        return redirect(url_for("main.index"))
    return render_template("/auth/form_template.html", form=form, title=title)

# 重设密码，邮箱定向来， 修改密码后转向登录界面
@auth.route("/resetpassword/<username>/<token>", methods=["GET", "POST"])
def reset_password(username, token):
    title = "重设密码"
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if user.confirm(token):
                user.password = form.password.data
                flash("Reset successful")
                return redirect(url_for("auth.signin"))
        flash("Confrim fail")
    return render_template("/auth/form_template.html", form=form, title=title)

#  新用户邮箱确认， 重定向至首页，提示确认是否成功
@auth.route('/confirmation/<token>')
@login_required
def confirmation(token):
    if current_user.confirmed:
        flash("Your account has confirmed")
    elif current_user.confirm(token):
        current_user.confirmed = True
        db.session.commit()
        flash("Confirm successfully")
    else:
        flash("Confirmation fail")
    return redirect(url_for("main.index"))

# 更改密码，登录状态可用，更改后需重新登录
@auth.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
    title = "更改密码"
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_app.password = form.password.data
            db.session.commit()
            flash("Password changed")
            logout_user()
            return redirect(url_for("auth.signin"))
        flash("Password is wrong")
    return render_template("/auth/form_template.html", form=form, title=title)

# 更改邮箱地址，登录状态可用，更改后需要重新确认用户
@auth.route("/change_email", methods=['GET','POST'])
@login_required
def change_email():
    title = "变更邮箱"
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data) and \
                not User.query.filter_by(email=form.new_email.data).first():
            current_user.email = form.new_email.data
            current_user.confirmed = False
            db.session.commit()
            token = current_user.generate_confirmation_token()
            send_mail(current_user.email, 'Confirmation', 'email_confirm', token=token)
            flash("Email changed. Check your email to  confirm your account")
            return redirect(url_for("main.index"))
        flash("Password is wrong or email has registered")
    return render_template("/auth/form_template.html", form=form, title=title)

# 更改用户资料，登录状态可用，资料表单可以为空
@auth.route("/change_user_data", methods=['GET','POST'])
@login_required
def change_user_data():
    title = "更改资料"
    form = ChangeUserDataForm()
    if form.validate_on_submit():
        data_changed = False
        if form.age.data:
            current_user.age = form.age.data
            data_changed = True
        if form.sex.data:
            current_user.sex = form.sex.data
            data_changed = True
        if form.home.data:
            current_user.home = form.home.data
            data_changed = True
        if data_changed:
            db.session.commit()
            flash("Your data has changed")
        return redirect(url_for("main.user", username=current_user.username))
    return render_template("/auth/form_template.html", form=form, title=title)