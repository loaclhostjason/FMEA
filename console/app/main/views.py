# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash
from flask_login import login_required, current_user

from . import main
from .forms import *
from .models import *
from ..base import Check
from ..read_config import ReadAppConfig
from sqlalchemy import or_
from ..base import pagination_result
from collections import defaultdict

'''
dashboard
'''


@main.route('/')
@login_required
def my_file_list():
    products = Product.query

    if not current_user.is_admin():
        products = products.filter_by(user_id=current_user.id)

    products = products.all()
    return render_template('main/my_file.html', products=products)


'''
页面 文件 创建
'''


@main.route('/file/create')
@login_required
def create_file():
    form = CreateProductForm()
    return render_template('main/create_edit_file.html', form=form)


'''
页面 文件 编辑
'''


@main.route('/file/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_file(product_id):
    form = CreateProductForm()
    process_list = ReadAppConfig().get_config()

    product = Product.query.get_or_404(product_id)
    return render_template('main/create_edit_file.html', form=form, product=product, process_list=process_list)


'''
页面 最近修改文件
'''


@main.route('/last/file/list')
@login_required
def last_file_list():
    products = Product.query

    if not current_user.is_admin():
        products = products.filter(user_id=current_user.get_id())

    products = pagination_result(products)
    return render_template('main/last_file.html', products=products)


@main.route('/update/password', methods=['POST'])
@login_required
def update_password():
    user = User.query.get_or_404(current_user.get_id())
    form_data = request.form.to_dict()
    if form_data['password2'] != form_data['password']:
        return jsonify({'success': False, 'message': '密码不一致'})

    user.password = form_data['password']
    db.session.add(user)
    return jsonify({'success': True, 'message': '更新成功'})


@main.after_request
def after_request(response):
    if not request.url_rule or request.method != 'POST':
        return response

    product_relation = ProductRelation.query.order_by(ProductRelation.timestamp.desc()).all()
    r = defaultdict(list)
    if product_relation:
        for pr in product_relation:
            r[pr.product_id].append(pr.timestamp)

    d = {k: max(v) for k, v in r.items() if v}
    if not d:
        return response

    for product_id, timestamp in d.items():
        product = Product.query.filter_by(id=product_id).first()
        if product and product.last_time < timestamp:
            product.last_time = timestamp
            db.session.add(product)
            db.session.commit()

    return response
