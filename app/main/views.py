from . import main
from flask import request, jsonify, render_template

from app.main.helper import DataTable
from app.models import Student


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/load')
def load():
    if request.method == 'GET':
        ret = DataTable(request, Student).output_result()
        return jsonify(ret)


