# coding: utf-8

from app.main.models import ProductRelation
from app import *
from collections import defaultdict


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

        for info in func_list:
            init_data = ['' for v in range(len(func_list) + 1)]

            init_data[0] = info.name
            init_data[1] = defaultdict(list)

            s_id = info.id
            s_func_list = data.get(s_id)
            if s_func_list:
                for s_info in s_func_list:
                    t_id = s_info.id
                    t_func_list = data.get(t_id)

                    init_data[1][s_info.name] = [v.name for v in t_func_list] if t_func_list else []

            result.append(init_data)

        return result

    # 再次转换 xml 需要的数据
    def get_func_xml(self):
        a = []
        for v in self.trans_data():
            for val in v:
                copy_data = v.copy()
                if isinstance(val, dict):
                    if val:
                        for key, info in val.items():
                            if info:
                                for vv in info:
                                    aa = copy_data.copy()
                                    aa[1] = key
                                    aa[2] = vv
                                    a.append(aa)
                            else:
                                bb = copy_data.copy()
                                bb[1] = key
                                a.append(bb)

                    else:
                        copy_data[1] = ''
                        copy_data[2] = ''
                        a.append(copy_data)

        return a