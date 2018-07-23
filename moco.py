from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort, flash, session, escape, json
from werkzeug import secure_filename
import os

from workingscript import process


app = Flask(__name__, static_folder='static')



# Relative path of directory for uploaded files/ Extensions allowed
UPLOAD_DIR = 'uploads/'
STATIC_DIR = 'static/'
PUBLIC_DIR = 'public/'
LOG_DIR = 'logs/'
ALLOWED_EXTENSIONS = set(['zip','dcm','jpg','nii'])

# Current path(s)
dir_path = os.path.dirname(os.path.realpath(__file__))
abs_upload_path = os.path.join(dir_path,UPLOAD_DIR)
abs_static_path = os.path.join(dir_path,STATIC_DIR)
abs_public_path = os.path.join(dir_path,STATIC_DIR,PUBLIC_DIR)

# Make upload, public dir, and logs dir if missing
if not os.path.isdir(abs_upload_path):
    os.mkdir(abs_upload_path)
if not os.path.isdir(abs_public_path):
    os.mkdir(abs_public_path)

# Setup misc
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR # Upload Directory
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS # Acceptable file types
app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024 # Max Size Currently: 2000MB
app.config['RESULT_FOLDER'] = STATIC_DIR+PUBLIC_DIR #place where changed files will be stored for downloading

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():

    valid_list = []

    if request.method == 'POST':
        uploaded_files = request.files.getlist("files")
        if uploaded_files[0].filename == '':
                flash('No files selected.', 'Error')
        else:
            for upload in uploaded_files:
                valid_list.append(allowed_file(upload.filename))
                if any(f == False for f in valid_list):
                    flash('File Extension not allowed.', 'Error')
                else:
                    for upload in uploaded_files:
                        filename = secure_filename(upload.filename)
                        upload.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))



                        #runs a custom script here!
                        process(abs_upload_path, abs_public_path, filename, '_corrected')
                    return redirect(url_for('processing'))


    return render_template('index.html')

@app.route('/processing')
def processing():
        #TODO: Implement the posibiliyty to send en email with the processed file



    return render_template('processing.html', image=app.config['RESULT_FOLDER']+os.listdir(abs_public_path)[0])
