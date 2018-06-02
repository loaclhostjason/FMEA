from . import help
from flask import render_template, redirect, url_for, request, abort, flash
from flask_login import login_required
from .forms import *
from ..base import Check, Tool
from .models import *
from ..decorators import role_required
from .func import *
import time
# from datetime import datetime

from config import Config
from ..app import upload_video

@help.route('/doc', methods=['GET', 'POST'])
@login_required
def doc_list():
    form = SelectHelpDocForm()

    docs_query = HelpFiles.query.order_by(HelpFiles.time.desc()).filter_by(type='doc')

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        form_data = form.get_form_data()
        return redirect(url_for('.doc_list', **form_data))

    page_params = {k: v for k, v in request.args.items() if v and k not in ['page']}

    docs = HelpFiles.filter_params(docs_query, page_params)

    form.set_form_data(page_params)
    return render_template('help/doc.html', form=form, docs=docs)


@help.route('/doc/create_edit_doc', methods=['GET', 'POST'])
@login_required
@role_required
def create_edit_doc():
    form = HelpDocForm()
    doc_id = request.args.get('doc_id')
    doc = HelpFiles.query.filter_by(id=doc_id).first()

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        old_doc = HelpFiles.query.filter_by(title=form.title.data, type='doc').first()
        if old_doc and old_doc.title != form.title.data:
            flash({'errors': '标题重复了'})
            return redirect(request.url)

        form_data = form.get_form_data()
        file = request.files.get('file')
        if not file:
            form_data['file'] = doc.file if doc else None
            form_data['file_name'] = doc.file_name if doc else None
        else:
            form_data['file'], form_data['file_name'] = upload_file(file, doc)

        if doc:
            form.populate_obj(doc)

        HelpFiles.edit_or_create_doc(form_data, doc)
        flash({'success': '更新成功！'})
        return redirect(url_for('.doc_list'))

    if doc:
        form.set_form_data(doc)
    return render_template('help/create_edit_doc.html', form=form, doc=doc)


@help.route('/doc/delete/<int:id>', methods=['POST'])
@login_required
def delete_doc(id):
    doc = HelpFiles.query.filter_by(id=id).first()
    if not doc:
        return jsonify({'success': False, 'message': '没有记录'})

    base_path = os.path.join(current_app.config['UPLOAD_DOC_DIR'], doc.time.strftime('%Y%m%d'))
    del_os_filename(base_path, doc.file)
    db.session.delete(doc)
    return jsonify({'success': True, 'message': '删除成功'})


@help.route('/download_file', methods=['GET', 'POST'])
@login_required
def download_files():
    filename = request.args.get("filename")
    time_str = request.args.get("time")
    if not time_str or not filename:
        abort(404)

    time_d = Tool.str_to_time(time_str)
    if filename:
        return download_file(filename, Tool.time_to_date(time_d, format='%Y%m%d'))


@help.route('/video', methods=['GET', 'POST'])
@login_required
def video_list():
    form = SelectHelpVideoForm()
    return render_template('help/video.html', form=form)


@help.route('/video/create_edit', methods=['GET', 'POST'])
@login_required
def create_edit_video():
    form = HelpVideoForm()
    video_id = request.args.get('doc_id')
    video = HelpFiles.query.filter_by(id=video_id, type='video').first()

    Check(form).check_validate_on_submit()
    if form.validate_on_submit():
        old_video = HelpFiles.query.filter_by(title=form.title.data, type='video').first()
        if old_video and old_video.title != form.title.data:
            flash({'errors': '标题重复了'})
            return redirect(request.url)

        form_data = form.get_video_form()
        HelpFiles.edit_or_create_video(form_data, video)
        flash({'success': '更新成功'})
        return redirect(url_for('.video_list'))

    return render_template('help/create_edit_video.html', form=form, video=video)
