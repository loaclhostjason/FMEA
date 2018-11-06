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
            init_data = ['' for v in range(len(func_list) + 22)]

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
            return [], [], [], []
        failure = AttrContent.query.filter(AttrContent.name_number.like(relation.name_number + '-FA%'),
                                           AttrContent.product_id == self.product_id).all()

        content_name = []
        content_s = []
        content_fm = []
        content_fc = []
        if failure:
            for info in failure:
                if info.real_content:
                    c = json.loads(info.real_content)

                    content_name.append(c['name'])
                    content_s.append(c.get('spec_num', ''))
                    content_fm.append(c.get('detection_device', ''))
                    content_fc.append(c.get('desciption', ''))

        # print(content)
        # name,
        return content_name, content_s, content_fm, content_fc

    def get_assess_data(self, func_id, action_type=None, type=None):
        relation = FuncRelation.query.filter(FuncRelation.product_relation_id == func_id,
                                             FuncRelation.product_id == self.product_id).all()

        content_12 = []
        content_13 = []
        content_14 = []
        content_15 = []
        content_16 = []
        content_17 = []
        content_18 = []

        if not relation:
            return content_12, content_13, content_14, content_15, content_16, content_17, content_18

        failure_id = [v.id for v in relation]
        assess = ProductAssess.query.filter(ProductAssess.func_relation_id.in_(failure_id)).all()

        if assess:
            for info in assess:
                if info.content:
                    c = json.loads(info.content)
                    content_12.append(c['name'])

        # print(content)
        return content_12, content_13, content_14, content_15, content_16, content_17, content_18

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
                    forth_data = self.filter_number(name_number[0]) or ''
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
                                    sec_data[5] = self.filter_number(name_number or '0') or ''
                                    sec_data[4] = self.filter_number(name_number[:-2] or '0') or ''

                                    # todo 8-10
                                    content_name, content_s, content_fm, content_fc = self.failure_relation(
                                        vv['id'], vv['number'])

                                    sec_data[6] = content_name or ''
                                    sec_data[7] = content_s or ''
                                    sec_data[8] = content_fm or ''
                                    sec_data[9] = content_fc or ''

                                    # todo 12 -18
                                    [
                                        content_12,
                                        content_13,
                                        content_14,
                                        content_15,
                                        content_16,
                                        content_17,
                                        content_18
                                    ] = self.get_assess_data(vv['id'], action_type='current')
                                    # print(vv['id'])
                                    sec_data[10] = content_12 or ''
                                    sec_data[11] = content_13 or ''
                                    sec_data[12] = content_14 or ''
                                    sec_data[13] = content_15 or ''
                                    sec_data[14] = content_16 or ''
                                    sec_data[15] = content_17 or ''
                                    sec_data[16] = content_18 or ''

                                    # todo 19 -23
                                    [
                                        content_19,
                                        content_20,
                                        content_21,
                                        content_22,
                                        content_23,
                                        content_24,
                                        content_25
                                    ] = self.get_assess_data(vv['id'], action_type='optimize')

                                    sec_data[17] = content_19 or ''
                                    sec_data[18] = content_20 or ''
                                    sec_data[19] = content_21 or ''
                                    sec_data[20] = content_22 or ''
                                    sec_data[21] = content_23 or ''
                                    sec_data[22] = content_24 or ''
                                    sec_data[23] = content_25 or ''

                                    a.append(sec_data)
                            else:
                                sec = copy_data.copy()
                                sec[1] = key

                                name_number = other_init[key]['name_number']
                                sec[4] = self.filter_number(name_number or '0') or ''

                                a.append(sec)

                    else:
                        copy_data[1] = ''
                        copy_data[2] = ''

                        copy_data[4] = ''
                        a.append(copy_data)

        # print(a)
        return a

    def test(self):
        data = self.get_func_xml()
        if not data:
            return

        _len = defaultdict(list)
        for index, val in enumerate(data):
            for v in val:
                if isinstance(v, list):
                    _len[index].append(len(v))
                else:
                    _len[index].append(0)
        max_len = {k: max(v) for k, v in _len.items()}

        # print(max_len)
        #
        # # todo
        result = []
        for index, val in enumerate(data):
            this_len = max_len[index]
            if this_len:
                # print(val)
                mult_val = [val] * this_len
                # print(mult_val)
                for i, v in enumerate(mult_val):
                    this_list = []
                    for info in v:
                        if isinstance(info, list):
                            try:
                                info = info[i]
                            except:
                                info = ''
                            this_list.append(info)
                        else:
                            this_list.append(info)
                    result.append(this_list)
                # print(result)
                # break
            else:
                result.append(val)
                # print(11, val)
        # print(result)
        return result
