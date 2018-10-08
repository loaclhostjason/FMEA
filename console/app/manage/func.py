from ..main.models import *
from .models import *
import json


def parent_info(parent_id):
    product_relation = ProductRelation.query.filter_by(id=parent_id).first()
    if product_relation:
        yield product_relation.id

        r = [v for v in list(parent_info(product_relation.parent_id)) if v]
        if r:
            for re in r:
                yield re


def children_info(id, product_id):
    children = ProductRelation.query.filter_by(parent_id=id, product_id=product_id).all()
    if children:
        for c in children:
            yield c.id

            r = [v for v in list(children_info(c.id, product_id)) if v]
            if r:
                for re in r:
                    yield re


def get_all_func(id, product_id, type, show_key, func_id=None):
    print(11, show_key)
    product_relation = ProductRelation.query.filter_by(id=id, product_id=product_id).first()
    if not product_relation:
        return

    # 父节点
    parent_list = list(parent_info(product_relation.parent_id))
    print(parent_list)

    # 子节点
    child_list = [v for v in list(children_info(id, product_id)) if v]
    print(child_list)

    result = []

    # todo more
    func = FuncRelation.query.filter_by(product_relation_id=id, type=type, product_id=product_id)
    if func_id:
        func = func.filter_by(id=func_id)
    func = func.first()
    # print(func.id)
    if not func:
        return result

    result.append({
        'color': 'green' if type == 'func' else 'red',
        'type': type,
        'name': func.name,
        'key': "Root",
        'is_show': True
    })

    result = get_parent_tree(parent_list, result, type, show_key)
    result = get_children_tree(child_list, result, type, show_key)

    print('result', result)
    return result


def get_parent_tree(parent_list, result, type, show_key):
    if parent_list:
        parent_func = FuncRelation.query.filter(FuncRelation.product_relation_id.in_(parent_list), FuncRelation.type == type).all()
        for info in parent_func:
            result.append({
                'parent': 'Root',
                'dir': "left",
                'color': 'green' if type == 'func' else 'red',
                'name': info.name,
                'key': info.name_number,
                'is_show': bool(info.name_number == show_key) if show_key is not False else False,
                'type': type,
            })
    print(show_key)
    return result


def get_children_tree(child_list, result, type, show_key):
    if child_list:
        child_func = FuncRelation.query.filter(FuncRelation.product_relation_id.in_(child_list), FuncRelation.type == type).all()
        for info in child_func:
            result.append({
                'parent': 'Root',
                'dir': "right",
                'color': 'green' if type == 'func' else 'red',
                'name': info.name,
                'key': info.name_number,
                'is_show':  bool(info.name_number == show_key) if show_key is not False else False,
                'type': type,
            })
    return result
