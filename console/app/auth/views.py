# coding: utf-8
from flask import render_template, redirect, url_for, abort, request, flash, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from . import auth
from .forms import *
from ..base import Check
from .. import db
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.my_file_list'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的帐户', 'auth/email/confirm', user=current_user, token=token)
    flash({'info': '一个新的确认电子邮件已经发送给你的电子邮件'})
    return redirect(url_for('main.my_file_list'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        old = User.query.filter_by(email=form.email.data).first()
        if old:
            flash({'errors': '已经注册了， 请登陆'})
            return redirect(request.url)

        register_form_data = form.get_form_data()
        del register_form_data['password2']
        user = User(**register_form_data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Accont', 'auth/email/confirm', user=user, token=token)

        flash({'success': '确认邮件已通过电子邮件发送给您'})
        return redirect(url_for('main.my_file_list'))

    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.my_file_list'))
    if current_user.confirm(token):
        flash({'success': '你已经确认了你的账户。谢谢！'})
    else:
        flash({'errors': '确认链接无效或已过期'})
    return redirect(url_for('main.my_file_list'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            current_user.update_time_ip()
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.my_file_list')
            return redirect(next)
        flash({'errors': '用户名或者密码错误！'})

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
