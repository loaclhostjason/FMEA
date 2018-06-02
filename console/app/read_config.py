# coding: utf-8
import os
import json
from flask import current_app
from collections import OrderedDict


class ReadConfig:
    def __init__(self):
        path = current_app.config['CONFIG_PATH']

        self.config_paths = list()
        for (root, dirs, files) in os.walk(path):
            for filename in files:
                r = {
                    'filename': os.path.splitext(filename)[0],
                    'root_path': os.path.join(root, filename),
                }
                self.config_paths.append(r)

    def get_all_config(self):
        return self.config_paths

    def choice_config_path(self, name):
        if not self.config_paths:
            return
        for path in self.config_paths:
            if path['filename'] == name:
                this_path = path['root_path']
                return this_path
        return

    def read_config_data(self, name):
        path = self.choice_config_path(name)
        if not path: return
        with open(path, encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data) if data else None
        return data


class ReadAppConfig:
    def __init__(self):
        self.path = current_app.config['APP_CONFIG_PATH']

    def get_config(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data)
        return data
