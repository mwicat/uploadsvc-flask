from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    render_template,
    redirect,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_prefixed_env()


def get_upload_path():
    return Path(app.config['UPLOAD_DIR'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated', False):
            return ''
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if session.get('authenticated', False):
        return redirect(url_for('upload_file'))
    else:
        return redirect(url_for('login'))


@app.route('/files/', methods=['GET'])
@login_required
def file_list():
    return render_template(
        'list_files.html', file_list=get_upload_path().iterdir())


@app.route('/files/<string:filename>', methods=['GET'])
@login_required
def file_get(filename):
    return send_file(get_upload_path() / secure_filename(filename))


@app.route('/push', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            f.save(get_upload_path() / secure_filename(f.filename))
        return 'ok'
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == app.config['UPLOAD_PASSWORD']:
            session['authenticated'] = True
            return redirect(url_for('upload_file'))
        else:
            session['authenticated'] = False
            return 'nope'
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session['authenticated'] = False
    return ''
