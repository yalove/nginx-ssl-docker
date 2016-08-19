from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, g,jsonify
import json
from werkzeug import secure_filename

upload = Blueprint("upload", __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config[
               'ALLOWED_EXTENSIONS']


@upload.route("/upload", methods=['GET', 'POST'])
def function():
	from .upload import QiNiuUpload
	qn = QiNiuUpload(current_app)
	files =[]
	if request.method == 'POST':
		uploaded_files = request.files.getlist("file[]")
		for file in uploaded_files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				filename = qn.save_data(filename,file)
				files.append(qn.get_data_url(filename))
	return render_template('upload.html',files=files)

@upload.route("/del")
def function1():
	from .upload import QiNiuUpload
	qn = QiNiuUpload(current_app)
	result = qn.del_data('11.txt')
	return jsonify(result=result)

@upload.route("/list")
def function2():
	from .upload import QiNiuUpload
	qn = QiNiuUpload(current_app)
	items = qn.list_data()
	return jsonify(items = items)