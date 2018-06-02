from . import temps
from flask_login import login_required
from flask import render_template


@temps.route('/list')
@login_required
def temps_list():
    return render_template('temps/index.html')
