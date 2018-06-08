from . import temps
from flask_login import login_required
from flask import render_template
from ..main.models import ProductRelation
from ..models import *

@temps.route('/list')
@login_required
def temps_list():
    print([v.to_dict() for v in ProductRelation.query])
    return render_template('temps/index.html')
