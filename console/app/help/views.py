from . import help
from flask import render_template


@help.route('/doc')
def doc_list():
    return render_template('help/doc.html')
