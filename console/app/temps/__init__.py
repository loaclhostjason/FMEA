# coding: utf-8

from flask import Blueprint

temps = Blueprint('temps', __name__)

from . import views, models
