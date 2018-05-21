# -*- coding: utf-8 -*-
from flask import Blueprint

contact = Blueprint('contact', __name__)

from . import views, models