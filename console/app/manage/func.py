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


def get_all_func(id, product_id, type):
    product_relation = ProductRelation.query.filter_by(id=id, product_id=product_id).first()
    if not product_relation:
        return

    # 父节点
    parent_list = list(parent_info(product_relation.parent_id))
    print(parent_list)

    # 子节点
    child_list = [v for v in list(children_info(id, product_id)) if v]
    print(child_list)

    result = {
        'nodedata': [],
        'linkdata': [],
    }

    # todo more
    func = FuncRelation.query.filter_by(product_relation_id=id, type=type, product_id=product_id).first()

    result['nodedata'].append({
        'category': 'SelfNode',
        'color': 'green' if type == 'func' else 'red',
        'name': func.name,
        'key': func.name_number
    })
    result = get_parent_tree(parent_list, result, func.name_number, type)
    result = get_children_tree(child_list, result, func.name_number, type)
    return result


def get_parent_tree(parent_list, result, name_number, type):
    if parent_list:
        parent_func = FuncRelation.query.filter(FuncRelation.product_relation_id.in_(parent_list), FuncRelation.type == type).all()
        for info in parent_func:
            result['nodedata'].append({
                'category': 'ParentNode',
                'color': 'green' if type == 'func' else 'red',
                'name': info.name,
                'key': info.name_number
            })
            result['linkdata'].append({
                'from': info.name_number,
                'to': name_number
            })
    return result


def get_children_tree(child_list, result, name_number, type):
    if child_list:
        child_func = FuncRelation.query.filter(FuncRelation.product_relation_id.in_(child_list), FuncRelation.type == type).all()
        for info in child_func:
            result['nodedata'].append({
                'category': 'ChilrenNode',
                'color': 'green' if type == 'func' else 'red',
                'name': info.name,
                'key': info.name_number
            })
            result['linkdata'].append({
                'from': name_number,
                'to': info.name_number
            })
    return result
