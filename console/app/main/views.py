# coding: utf-8
from flask import render_template, redirect, url_for, jsonify, abort, request, flash
from flask_login import login_required

from . import main
from .forms import *


@main.route('/main')
@main.route('/')
@login_required
def my_file_list():
    return render_template('main/my_file.html')


@main.route('/main/file/create')
@login_required
def create_file():
    form = CreateProductForm()
    return render_template('main/create_file.html', form=form)
