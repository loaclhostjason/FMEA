# coding: utf-8
from flask import request, jsonify
from .models import FuncRelation
from collections import defaultdict, OrderedDict


def get_func_relation(init_result, product_relation_id):
    if not product_relation_id:
        return init_result
    # result = {
    #     'nodedata': [],
    #     'linkdata': [],
    # }
    func_relation = FuncRelation.query.filter_by(product_relation_id=product_relation_id, type='func').all()
    if not func_relation:
        return init_result

    for index, fr in enumerate(func_relation):
        init_result['nodedata'].append({
            'category': 'FuncNode',
            'name': fr.name,
            'key': fr.id,
            'name_number': fr.name_number,
            'product_relation_id': product_relation_id
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


def get_failure_relation(result, parent_id):
    failure_relation = FuncRelation.query.filter_by(parent_id=parent_id, type='failure').all()
    if not failure_relation:
        return result

    for failure in failure_relation:
        result['nodedata'].append({
            'category': 'FailureNode',
            'name': failure.name,
            'key': failure.id,
            'name_number': failure.name_number
        })
        d = {
            'category': 'FailureLink',
            'from': parent_id,
            'to': failure.id
        }
        result['linkdata'].append(d)

    return result


def export_excel(product_data):
    export_result = defaultdict(list)

    for contract, contract_type_name in product_data:
        export_result['产品'].append(contract.contract_id)
        export_result['签约日期'].append(contract.sign_date.strftime("%Y-%m-%d"))
        export_result['合同类型'].append(contract_type_name)
        export_result['最终用户'].append(contract.end_user_name)
        export_result['合同金额'].append(contract.amount)
        export_result['产品'].append('%s个' % contract.product_count if contract.product_count else '--')

    column_names = ['合同号', '签约日期', '合同类型', '最终用户', '区域', '省份', '合同金额', '产品', '安装记录', '服务记录']
    new_excel_data = OrderedDict()
    for v in column_names:
        new_excel_data[v] = export_result[v]
    filename = u"%s年合同列表信息" % 'xx'

    return new_excel_data, filename
