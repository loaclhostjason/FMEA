# coding: utf-8
from flask import jsonify, request, make_response, send_file, abort, current_app
import os
import datetime


def del_os_filename(base_path, filename):
    for root, dirs, files in os.walk(base_path, topdown=False):
        for name in files:
            if filename and filename == name:
                os.remove(os.path.join(root, name))


def upload_file(file, data):
    path = os.path.join(current_app.config['UPLOAD_DOC_DEST'])
    now_day = datetime.datetime.now().strftime('%Y%m%d')
    base_path = os.path.join(path, now_day)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if data:
        old_path = os.path.join(path, data.time.strftime('%Y%m%d'))
        del_os_filename(old_path, data.file)

    filename_list = os.path.splitext(file.filename)
    now = datetime.datetime.now().strftime('%H%M%S')
    save_filename = filename_list[0] + '_' + now + filename_list[-1]
    print(os.path.join(base_path, save_filename))
    file.save(os.path.join(base_path, save_filename))
    return save_filename, file.filename


def download_file(filename, extra_path=None):
    try:
        from urllib.parse import quote

        if extra_path:
            filename_path = os.path.join(current_app.config['UPLOAD_DOC_DEST'], extra_path, filename)
        else:
            filename_path = os.path.join(current_app.config['UPLOAD_DOC_DEST'], filename)

        response = make_response(send_file(filename_path, as_attachment=True))
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=quote(filename.encode('utf-8'))
            )
        return response
    except Exception as e:
        print(e)
        abort(404)
