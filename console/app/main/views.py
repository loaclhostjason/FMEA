# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash
from flask_login import login_required

from . import main
from .forms import *
from .models import *
from ..base import Check
from ..read_config import ReadAppConfig


@main.route('/')
@login_required
def my_file_list():
    products = Product.query.all()
    return render_template('main/my_file.html', products=products)


@main.route('/file/create')
@login_required
def create_file():
    form = CreateProductForm()
    return render_template('main/create_edit_file.html', form=form)


@main.route('/file/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_file(product_id):
    form = CreateProductForm()
    edit_form = StructureTreeForm()

    process_list = ReadAppConfig().get_config()
    print(process_list)

    action = request.args.get('action')
    product = Product.query.get_or_404(product_id)

    if action == 'edit_attr':
        Check(form).check_validate_on_submit()
        if edit_form.validate_on_submit():
            edit_form.populate_obj(product)
            flash({'success': '更新成功'})
            return redirect(request.url)

        edit_form.set_form_data(product)
        return render_template('main/create_edit_file.html', form=form, product=product, edit_form=edit_form, process_list=process_list)

    return render_template('main/create_edit_file.html', form=form, product=product)
