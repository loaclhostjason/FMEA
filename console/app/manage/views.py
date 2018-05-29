from . import manage
from flask_login import login_required
from flask import render_template
from ..decorators import role_required


@manage.route('/config/list')
@login_required
@role_required
def config_list():
    return render_template('manage/config.html')
