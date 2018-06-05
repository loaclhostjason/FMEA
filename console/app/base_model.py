# coding: utf-8
from flask_sqlalchemy import Model


class BaseModel(Model):
    @staticmethod
    def update_model(model, data):
        if not data:
            return False

        if isinstance(data, dict):
            for k, v in data.items():
                setattr(model, k, v)

    @staticmethod
    def enum_to_value(data):
        if not data:
            new_data = None
            return new_data

        try:
            new_data = data.value
        except Exception as e:
            new_data = data
        return new_data

    @staticmethod
    def enum_to_name(data):
        if not data:
            new_data = None
            return new_data

        try:
            new_data = data.name
        except Exception as e:
            new_data = data
        return new_data

    def to_dict(self, extra_kw=None, extra_dict=None, remove_key=list()):
        model_field = [v for v in self.__dict__.keys() if not v.startswith('_') and v not in remove_key]
        result = dict()
        for info in model_field:
            result[info] = self.enum_to_value(getattr(self, info))

        if extra_kw and isinstance(extra_kw, list):
            for info in extra_kw:
                result[info] = self.enum_to_value(getattr(self, info))

        if extra_dict and isinstance(extra_dict, dict):
            for k, v in extra_dict.items():
                result[k] = v

        return result

    def to_dict_name(self):
        model_field = [v for v in self.__dict__.keys() if not v.startswith('_')]
        result = dict()
        for info in model_field:
            result[info] = self.enum_to_name(getattr(self, info))

        return result
