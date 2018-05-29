# coding: utf-8
from flask import request, jsonify
from .models import FuncRelation, FailureRelation


def get_func_relation(init_result, product_relation_id):
    if not product_relation_id:
        return init_result
    # result = {
    #     'nodedata': [],
    #     'linkdata': [],
    # }
    func_relation = FuncRelation.query.filter_by(product_relation_id=product_relation_id).all()
    if not func_relation:
        return init_result

    for index, fr in enumerate(func_relation):
        init_result['nodedata'].append({
            'category': 'FuncNode',
            'name': fr.name,
            'key': fr.id
        })

        init_result = get_failure_relation(init_result, fr.id)
        # d = {
        #     'category': 'FuncLink',
        # }
        # if len(func_relation) >= 2 and index < len(func_relation) - 1:
        #     d['from'] = fr.id
        #     d['to'] = func_relation[index + 1].id
        # init_result['linkdata'].append(d)

    return init_result


def get_failure_relation(result, func_relation_id):
    failure_relation = FailureRelation.query.filter_by(func_relation_id=func_relation_id).all()
    if not failure_relation:
        return result

    for failure in failure_relation:
        result['nodedata'].append({
            'category': 'FailureNode',
            'name': failure.name,
            'key': failure.id
        })
        d = {
            'category': 'FailureLink',
            'from': func_relation_id,
            'to': failure.id
        }
        result['linkdata'].append(d)

    return result
