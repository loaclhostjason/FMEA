# coding: utf-8

from app.main.models import *
from app.manage.models import *
from app import *
from collections import defaultdict
import json


class XmlData(object):
    def __init__(self, func_id):
        self.result = defaultdict(list)

        self.product_id = func_id

    def __get_parent_func_relation(self):
        func_relation = ProductRelation.query.filter_by(parent_id=self.product_id).all()
        # print(func_relation)
        self.result = defaultdict(list)
        if func_relation:
            for fr in func_relation:
                self.result[fr.parent_id].append(fr)
                self.__get_child_func_relation(self.result, fr.id)
        if not func_relation:
            # print(result)
            return self.result

    def __get_child_func_relation(self, result, id):
        child = ProductRelation.query.filter_by(parent_id=id).all()
        if child:
            for c in child:
                result[c.parent_id].append(c)
                self.__get_child_func_relation(result, c.id)

    # 转化一下 func relation 关系数据
    def trans_data(self):
        self.__get_parent_func_relation()
        data = self.result
        func_list = data.get(self.product_id)

        result = []

        other_init = dict()

        for info in func_list:
            init_data = ['' for v in range(len(func_list) + 10)]

            init_data[0] = {info.name: info.to_dict()}
            init_data[1] = defaultdict(list)

            s_id = info.id
            s_func_list = data.get(s_id)
            if s_func_list:
                for s_info in s_func_list:
                    t_id = s_info.id
                    t_func_list = data.get(t_id)

                    init_data[1][s_info.name] = [v.to_dict() for v in t_func_list] if t_func_list else []
                    init_data[1] = dict(init_data[1])

                    other_init[s_info.name] = s_info.to_dict()

            if not init_data[1]:
                init_data[1] = dict()

            result.append(init_data)

        return result, other_init

    def filter_number(self, name_number):
        attr_content = AttrContent.query.filter_by(product_id=self.product_id, type='func').filter(
            AttrContent.name_number.like(name_number + '-FU' + '%')).all()
        content = []
        if attr_content:
            for info in attr_content:
                if info.real_content:
                    c = json.loads(info.real_content)
                    content.append(c['name'])

        # print(11, content)
        return content

    def failure_relation(self, func_id, number):
        relation = FuncRelation.query.filter(FuncRelation.product_relation_id == func_id, FuncRelation.number == number,
                                             FuncRelation.product_id == self.product_id).first()

        if not relation:
            return []
        failure = AttrContent.query.filter(AttrContent.name_number.like(relation.name_number + '-FA%'),
                                           AttrContent.product_id == self.product_id).all()

        content = []
        if failure:
            for info in failure:
                if info.real_content:
                    c = json.loads(info.real_content)
                    content.append(c['name'])

        # print(content)
        return content

    # 再次转换 xml 需要的数据
    def get_func_xml(self):
        final_data, other_init = self.trans_data()

        a = []
        for v in final_data:

            forth_data = ''
            for index, val in enumerate(v):
                copy_data = ['' for v in range(len(v))].copy()

                # 第一个节点
                copy_data[0] = list(dict(v[0]).keys())[0]

                # print('one', v)
                # 第四个节点
                if index == 0:
                    name_number = list(set([v['name_number'] for v in dict(val).values()]))
                    forth_data = ','.join(self.filter_number(name_number[0]))
                copy_data[3] = forth_data

                # 第二个 三个 节点 5 he 6
                if index == 1:
                    if val:
                        for key, info in dict(val).items():
                            if info:
                                for vv in info:
                                    sec_data = copy_data.copy()
                                    sec_data[1] = key
                                    sec_data[2] = vv['name']

                                    name_number = vv['name_number']
                                    sec_data[5] = ','.join(self.filter_number(name_number or '0'))
                                    sec_data[4] = ','.join(self.filter_number(name_number[:-2] or '0'))

                                    # todo 8-10
                                    sec_data[6] = ','.join(self.failure_relation(vv['id'], vv['number']))
                                    sec_data[7] = ','.join(self.failure_relation(vv['id'], vv['number']))

                                    print(vv['id'])

                                    a.append(sec_data)
                            else:
                                sec = copy_data.copy()
                                sec[1] = key

                                name_number = other_init[key]['name_number']
                                sec[4] = ','.join(self.filter_number(name_number or '0'))

                                a.append(sec)

                    else:
                        copy_data[1] = ''
                        copy_data[2] = ''

                        copy_data[4] = ''
                        a.append(copy_data)

        print(a)
        return a
