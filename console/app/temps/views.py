from . import temps
from flask_login import login_required
from flask import render_template, jsonify
from ..main.models import ProductRelation
from .models import *


@temps.route('/list')
@login_required
def temps_list():
    temps = Temps.query.filter_by(parent_id=None).all()
    return render_template('temps/index.html', temps=temps)


@temps.route('/view/<int:id>')
@login_required
def temps_view(id):
    temp = Temps.query.filter_by(id=id).first()
    return render_template('temps/view_temp.html', temp=temp)


@temps.route('/view/info/<int:id>')
@login_required
def temps_view_info(id):
    init_data = {
        'nodedata': [],
        'linkdata': [],
    }
    temp = Temps.query.filter_by(id=id).first()
    if not temp:
        return jsonify({'success': True, 'data': init_data})

    init_data['nodedata'].append({'name': temp.name, 'key': temp.id, 'name_number': temp.name_number})

    children = Temps.query.filter_by(parent_id=temp.id).all()
    if children:
        for child in children:
            init_data['nodedata'].append({'name': child.name, 'key': child.id, 'name_number': child.name_number})
            init_data['linkdata'].append({'from': temp.id, 'to': child.id})

    return jsonify({'success': True, 'data': init_data})
