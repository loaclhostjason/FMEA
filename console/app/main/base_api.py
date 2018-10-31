from . import main
from flask import jsonify, request, abort, current_app
from flask_login import current_user, login_required
from ..main.models import *
from datetime import datetime


def delete_product_children(id):
    relations = ProductRelation.query.filter_by(parent_id=id).all()
    if not relations:
        return

    for relation in relations:
        next_id = relation.id
        db.session.delete(relation)
        db.session.commit()

        delete_product_children(next_id)


def delete_func_children(id):
    relations = FuncRelation.query.filter_by(parent_id=id).all()
    if not relations:
        return

    for relation in relations:
        db.session.delete(relation)
        db.session.commit()


@main.route('/tree/delete/<int:id>', methods=['POST'])
@login_required
def del_tree(id):
    type = request.args.get('type')
    if not type:
        product_relation = ProductRelation.query.filter_by(id=id).first()
        if not product_relation:
            return jsonify({'success': False, 'message': '没有此记录'})
        if not product_relation.parent_id:
            return jsonify({'success': False, 'message': '这节点为根节点，不支持删除'})
        db.session.delete(product_relation)
        delete_product_children(id)
        return jsonify({'success': True, 'message': '更新成功'})

    else:
        func_relation = FuncRelation.query.filter_by(id=id).first()
        if not func_relation:
            return jsonify({'success': False, 'message': '没有此记录'})

        product_relation_id = func_relation.product_relation_id
        db.session.delete(func_relation)
        delete_func_children(id)
        return jsonify({'success': True, 'message': '更新成功', 'product_relation_id': product_relation_id})


@main.route('/tree/edit/name', methods=['POST'])
@login_required
def edit_tree_name():
    from ..help.func import del_os_filename
    type = request.form.get('type')

    name = request.form.get('name')
    id = request.form.get('id')
    if not name:
        return jsonify({'success': False, 'message': '名称不能为空'})

    if not type:
        product_relation = ProductRelation.query.filter_by(id=id).first()
        if product_relation.level == 0:
            del_os_filename(current_app.config['UPLOADS_XML_DEST'], '%s.xls' % product_relation.name)

        if not product_relation:
            return jsonify({'success': False, 'message': '没有此记录'})

        if not product_relation.parent_id:
            old_product = Product.query.filter_by(name=name).first()
            if old_product:
                return jsonify({'success': False, 'message': '名称已经存在'})

            product = Product.query.filter_by(name=product_relation.name).first()
            product.name = name
            db.session.add(product)

        product_relation.name = name
        product_relation.timestamp = datetime.now()
        db.session.add(product_relation)
        return jsonify({'success': True, 'message': '更新成功', 'product_relation_id': None})

    else:
        func_relation = FuncRelation.query.filter_by(id=id).first()
        if not func_relation:
            return jsonify({'success': False, 'message': '没有此记录'})

        func_relation.name = name
        db.session.add(func_relation)

        product_relation_id = func_relation.product_relation_id
        return jsonify({'success': True, 'message': '更新成功', 'product_relation_id': product_relation_id})
