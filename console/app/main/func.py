# coding: utf-8
from flask import request, jsonify
from .models import FuncRelation
from collections import defaultdict, OrderedDict
from .models import *
from ..manage.models import *
import json


def get_func_relation(init_result, product_relation_id):
    if not product_relation_id:
        return init_result

    product_relation = ProductRelation.query.filter_by(id=product_relation_id).first()
    if not product_relation:
        return init_result

    init_result['nodedata'].append({'category': 'ProductNode',
                                    'name': product_relation.name,
                                    'type': 'product',
                                    'key': 'product_node_%s' % product_relation_id,
                                    'name_number': product_relation.name_number})
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
        init_result['linkdata'].append({
            'from': 'product_node_%s' % product_relation_id,
            'to': fr.id,
            'category': 'ProductLink'
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


def export_excel(product_id):
    export_result = defaultdict(list)

    column_names = [
        '过程项目', '过程步骤', '过程作业要素',
        '过程项目功能', '过程步骤功能', '过程作业要素功能',
        '过程项目失效', '过程步骤失效', '过程作业要素失效',
        '当前风险分析S评估', '当前风险分析O评估', '当前风险分析D评估',
        '优化风险分析S评估', '优化风险分析O评估', '优化风险分析D评估',
        '负责人'
    ]
    product_relation = ProductRelation.query.filter(ProductRelation.product_id == product_id, ProductRelation.level == 1).all()

    product = Product.query.filter(Product.id == product_id).first()
    if not product_relation:
        return False

    for pr in product_relation:
        child = ProductRelation.query.filter_by(parent_id=pr.id, level=2).all()
        export_result['过程项目'].append(pr.name)
        export_result['过程步骤'].append('')
        export_result['过程作业要素'].append('')
        export_result = get_exceal_pre(export_result, pr, product_id, False)
        export_result['负责人'].append(product.user.username)

        if child:

            for c in child:
                child_next = ProductRelation.query.filter_by(parent_id=c.id, level=3).all()

                export_result['过程项目'].append(pr.name)
                export_result['过程步骤'].append(c.name)
                export_result['过程作业要素'].append('')
                export_result = get_exceal_pre(export_result, c, product_id, False)
                export_result['负责人'].append(product.user.username)

                if child_next:
                    for next in child_next:
                        export_result['过程项目'].append(pr.name)
                        export_result['过程步骤'].append(c.name)
                        export_result['过程作业要素'].append(next.name)
                        export_result = get_exceal_pre(export_result, next, product_id, True)

                        export_result['负责人'].append(product.user.username)

    new_excel_data = OrderedDict()
    for v in column_names:
        new_excel_data[v] = export_result[v]
    filename = u"%s--分析报告" % product.name

    return new_excel_data, filename


def get_exceal_pre(export_result, info, product_id, show):
    first_func = []
    first_failure = []
    if get_func_data(info.id, 'func'):
        first_func, first_failure = get_func_data(info.id, 'func')

    s_first = get_assess_data(product_id, 's', info.name_number, 'current')
    O_first = get_assess_data(product_id, 'O', info.name_number, 'current')
    D_first = get_assess_data(product_id, 'D', info.name_number, 'current')

    s_x = get_assess_data(product_id, 's', info.name_number, 'optimize')
    O_x = get_assess_data(product_id, 'O', info.name_number, 'optimize')
    D_xt = get_assess_data(product_id, 'D', info.name_number, 'optimize')

    export_result['过程项目失效'].append(';'.join(first_func))
    export_result['过程步骤失效'].append(';'.join(first_failure) if not show else [])
    export_result['过程作业要素失效'].append(';'.join(first_failure) if show else [])
    export_result['当前风险分析S评估'].append(['【{}:{}】'.format(v['name'], v['value']) for v in s_first])
    export_result['当前风险分析O评估'].append(['【{}:{}】'.format(v['name'], v['value']) for v in O_first])
    export_result['当前风险分析D评估'].append(['【{}:{}】'.format(v['name'], v['value']) for v in D_first])

    export_result['优化风险分析S评估'].append(['【{}:{}】'.format(v['name'], v['value']) for v in s_x])
    export_result['优化风险分析O评估'].append(['【{}:{}】'.format(v['name'], v['value']) for v in O_x])
    export_result['优化风险分析D评估'].append(['【{}:{}】'.format(v['name'], v['value']) for v in D_xt])

    return export_result


def get_func_data(product_relation_id, type):
    func = FuncRelation.query.filter_by(product_relation_id=product_relation_id, type=type)
    func = func.all()

    result = []
    fail = []
    if not func:
        return result
    for r in func:
        result.append(r.name)
        failure = FuncRelation.query.filter(FuncRelation.parent_id == r.id, FuncRelation.type == 'failure').all()
        if failure:
            for fa in failure:
                fail.append(fa.name)
    return result, fail


def get_assess_data(product_id, assess, name_number, type):
    product_assess = ProductAssess.query.filter_by(product_id=product_id, assess=assess, name_number=name_number, type=type).first()
    result = []
    if not product_assess:
        return []
    assess_type = {
        'name': '名称',
        'current_assess': '发生度评估',
        'ap_priority': 'AP行动优先级',
        'description': '备注',
        'help': '帮助',
    }
    if product_assess.content:
        content = json.loads(product_assess.content)
        for k, v in content.items():
            if assess_type.get(k) and v:
                result.append({
                    'name': assess_type[k],
                    'value': v
                })
    print(result)
    return result
