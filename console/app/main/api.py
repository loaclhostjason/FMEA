# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash, make_response, send_file, \
    current_app
from flask_login import login_required, current_user

from . import main
from .forms import *
from .. import db
from .models import *
from ..read_config import ReadConfig
from datetime import datetime

from .func import get_func_relation, get_failure_relation
from ..read_config import ReadAppConfig
from collections import defaultdict
import json
from sqlalchemy import or_
from ..manage.models import AttrContent, ProductAssess
from ..app import excel
import xlwt
import os
from config import Config

'''
process 
'''


@main.route('/process')
@login_required
def prcess_list():
    process_list = ReadAppConfig().get_config()
    process_list = sorted(process_list.items(), key=lambda d: d[1]['id'])
    result = []
    for k, v in process_list:
        result.append({k: dict(v)})
    return jsonify({'success': True, 'data': result})


'''
我的文件 delete
'''


@main.route('/file/product/delete/<int:id>', methods=['POST'])
def delete_file(id):
    from ..help.func import del_os_filename
    product = Product.query.get_or_404(id)

    del_os_filename(current_app.config['UPLOADS_XML_DEST'], '%s.xls' % product.name)

    db.session.delete(product)
    return jsonify({'success': True, 'message': '删除成功'})


'''
我的文件 create
'''


@main.route('/file/product/create', methods=['POST'])
@login_required
def create_file_product():
    form_data = request.form.to_dict()
    if not form_data.get('name'):
        return jsonify({'success': False, 'message': '产品名称不能为空'})

    product = Product.query.filter_by(name=form_data['name']).first()
    if product:
        return jsonify({'success': False, 'message': '产品名称重复'})

    d = {
        'name': form_data['name'],
        'user_id': current_user.get_id(),
    }

    add_product = Product(**d)
    db.session.add(add_product)
    db.session.flush()

    product_id = add_product.id

    product_relation = {
        'name': form_data['name'],
        'level': 0,
        'name_number': 0,
        'product_id': product_id
    }

    relation = ProductRelation(**product_relation)
    db.session.add(relation)
    return jsonify({'success': True, 'message': '更新成功', 'product_id': product_id})


# @main.route('/file/product/create', methods=['POST'])
# @login_required
# def create_file_product():
#     form_data = request.form.to_dict()
#     if not form_data.get('config_name'):
#         return jsonify({'success': False, 'message': '没有选择配置文件'})
#
#     config_data = ReadConfig().read_config_data(form_data['config_name'])
#
#     product = Product.query.filter_by(config_name=form_data['config_name']).first()
#     if product:
#         return jsonify({'success': False, 'message': '添加过，请编辑'})
#
#     d = dict({
#         'config_name': form_data['config_name'],
#         'file_name': '%s_%s' % (form_data['config_name'], datetime.now().strftime('%Y-%m-%d'))
#     }, **config_data)
#
#     d['user_id'] = current_user.get_id()
#     add_product = Product(**d)
#     db.session.add(add_product)
#     db.session.flush()
#
#     product_id = add_product.id
#     return jsonify({'success': True, 'message': '更新成功', 'product_id': product_id})


'''
我的文件 树
'''


@main.route('/file/tree')
@login_required
def get_file_tree():
    result = {
        'nodedata': [],
        'linkdata': [],
    }

    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({'success': False, 'message': '没有获取到配置文件信息'})

    product = ProductRelation.query.filter_by(product_id=product_id).order_by(ProductRelation.relation_order,
                                                                              ProductRelation.id).all()
    if not product:
        return jsonify({'success': True, 'data': result})

    link_data = []
    for rl in product:
        # if rl.parent_id != product_id:
        if rl.parent_id:
            link_data.append({'from': rl.parent_id, 'to': rl.id})

        result['nodedata'].append({
            'name': rl.name,
            'key': rl.id,
            'level': rl.level + 1,
            'name_number': rl.name_number,
        })

    result['linkdata'] = link_data
    return jsonify({'success': True, 'data': result})


@main.route('/file/func/failure/tree')
@login_required
def get_file_func_tree():
    result = {
        'nodedata': [],
        'linkdata': [],
    }

    product_relation_id = request.args.get('product_relation_id')
    if not product_relation_id:
        return jsonify({'success': False, 'messgae': 'id 不存在'})

    result = get_func_relation(result, product_relation_id)
    return jsonify({'success': True, 'data': result})


'''
我的文件 儿子节点添加
'''


def get_copy_parent_id(key, type_name):
    copy_parent_id = None
    if key and not type_name:
        product_info = ProductRelation.query.filter_by(id=key).first()
        copy_parent_id = product_info.parent_id
        if not copy_parent_id:
            return {'success': False, 'message': '第一个不能被复制'}
    if key and type_name:
        func_info = FuncRelation.query.filter_by(id=key).first()
        copy_parent_id = func_info.parent_id

    return copy_parent_id


# key is no_copy_id
def copy_product_children(no_copy_id, copy_result_id):
    parent_id = copy_result_id[0]
    product_relation = ProductRelation.query.filter_by(parent_id=no_copy_id).all()
    if not product_relation:
        return

    for v in product_relation:
        d = {
            'parent_id': parent_id,
            'product_id': v.product_id,
            'level': int(v.level),
        }
        copy_result_id = ProductRelation.add_product_relation(d, v.name, v.product_id)
        if not copy_result_id:
            return
        copy_product_children(v.id, copy_result_id)


# key is no_copy_id
def copy_func_children(no_copy_id, copy_result_id):
    parent_id = copy_result_id[0]
    print(no_copy_id)
    func_relation = FuncRelation.query.filter_by(parent_id=no_copy_id).all()
    if not func_relation:
        return

    for v in func_relation:
        d = {
            'parent_id': parent_id,
            'product_id': v.product_id,
            'product_relation_id': v.product_relation_id,
        }
        print(d)
        FuncRelation.add_func_relation(d, v.name, 'failure')


@main.route('/file/tree/content/add/<int:id>', methods=['POST'])
@login_required
def add_file_tree_content(id):
    key = request.args.get('key')
    action = request.args.get('action')

    form_data = request.form.to_dict()
    parent_id = form_data.get('parent_id')

    copy_parent_id = get_copy_parent_id(key, form_data.get('type'))
    if isinstance(copy_parent_id, dict):
        return jsonify(copy_parent_id)

    if not form_data.get('content'):
        return jsonify({'success': False, 'message': '内容不能为空'})

    d = {
        'parent_id': parent_id if not copy_parent_id else copy_parent_id,
        'product_id': id,
    }

    product_relation_id = form_data.get('product_relation_id')

    # func | failure
    print(form_data.get('type'))
    if form_data.get('type'):
        d['product_relation_id'] = product_relation_id
        copy_result_id = FuncRelation.add_func_relation(d, form_data.get('content'), form_data.get('type'))
        if copy_result_id and action == 'copy':
            copy_func_children(key, copy_result_id)

    else:
        d['level'] = int(form_data['level']) if form_data.get('level') else None
        copy_result_id = ProductRelation.add_product_relation(d, form_data.get('content'), id)

        if copy_result_id and action == 'copy':
            copy_product_children(key, copy_result_id)

    return jsonify({'success': True, 'type': form_data.get('type'), 'product_relation_id': product_relation_id})


'''
属性接口
'''


@main.route('/tree/attr')
@login_required
def get_tree_attr():
    # get attr 参数
    level = request.args.get('level')
    type_name = request.args.get('type_name')
    name_number = request.args.get('name_number')
    product_id = request.args.get('product_id')

    attr = Attr.query.filter(Attr.name_number == name_number).first()
    if not attr:
        attr = Attr.query.filter(or_(Attr.level == level if level else False, Attr.type == type_name)).first()

    if not attr or not product_id:
        return jsonify({'success': False, 'messgae': '参数不对'})

    data = None
    content = None
    if attr.content:
        data = json.loads(attr.content)

    attr_content_query = AttrContent.query.filter(AttrContent.product_id == product_id)
    attr_content = attr_content_query.filter(AttrContent.name_number == name_number).first()

    if attr_content and attr_content.real_content:
        content = json.loads(attr_content.real_content)

    return jsonify({'success': True, 'data': data, 'content': content})


@main.route('/tree/attr/action')
@login_required
def get_tree_attr_action():
    type = request.args.get('type')
    action_type = request.args.get('action_type')
    func_relation_id = request.args.get('func_relation_id')

    attr_action = AttrOther.query.first()

    if not attr_action:
        return jsonify({'success': False, 'messgae': '参数不对'})

    data = json.loads(attr_action.content)
    data_action = ProductAssess.query.filter_by(type=type, action_type=action_type,
                                                func_relation_id=func_relation_id).first()

    content = None
    if data_action and data_action.content:
        content = json.loads(data_action.content)

    return jsonify({'success': True, 'data': data, 'content': content})


@main.route('/export/product/<int:product_id>')
@login_required
def exprot_product(product_id):
    # from .func import export_excel

    #
    # excel_data, filename = export_excel(product_id)
    # return excel.make_response_from_dict(excel_data, "xls", file_name=filename)

    from export_xml import ExportXml
    func_info = Product.query.filter_by(id=product_id).first()

    export_xml = ExportXml(product_id, func_info.name)
    export_xml.run()

    try:
        from urllib.parse import quote

        path = Config.UPLOADS_XML_DEST
        file_path = os.path.join(path, '%s.xls' % func_info.name)
        file_name = '%s.xls' % func_info.name

        response = make_response(send_file(file_path, as_attachment=True))
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=quote(file_name.encode('utf-8'))
            )
        return response
    except Exception as e:
        print(e)
        abort(404)


@main.route('/product/relation', methods=['POST'])
@login_required
def update_product_relation_order():
    id = request.args.get('id')

    type = request.args.get('type')
    if not id or not type:
        return jsonify({'success': False, 'message': '参数不对'})
    print(type)

    product_relation = ProductRelation.query.filter_by(id=id).first()
    if not product_relation:
        return jsonify({'success': False, 'message': '没有记录'})
    parent_id = product_relation.parent_id

    if type == 'up':
        prev_product_relation = ProductRelation.query.filter_by(parent_id=parent_id,
                                                                relation_order=product_relation.relation_order - 1).first()
        if not prev_product_relation:
            return jsonify({'success': False, 'message': '不能上移'})

        pre_order = prev_product_relation.relation_order + 1
        this_order = prev_product_relation.relation_order

        prev_product_relation.relation_order = pre_order
        product_relation.relation_order = this_order

        return jsonify({'success': True, 'message': '更新成功'})

    else:
        next_product_relation = ProductRelation.query.filter_by(parent_id=parent_id,
                                                                relation_order=product_relation.relation_order + 1).first()
        if not next_product_relation:
            return jsonify({'success': False, 'message': '不能下移'})

        next_order = next_product_relation.relation_order - 1
        this_order = next_product_relation.relation_order

        next_product_relation.relation_order = next_order
        product_relation.relation_order = this_order

        return jsonify({'success': True, 'message': '更新成功'})
