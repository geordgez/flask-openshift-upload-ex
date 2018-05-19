from sampleapp import myapp

import os

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from sampleapp.scripts.delete_letter import delete_letter

UPLOAD_FOLDER = './data/input'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

myapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Application routes
@myapp.route('/')
def helloworld():
    return 'Hello World!'

@myapp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(myapp.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template(
        'upload.html'
    )

@myapp.route('/letter_deleter')
def letter_deleter():
    '''
    Replaces all letters in a text file in the data/input folder
    '''

    # make sure there's an uploaded file
    upload_folder_path = './data/input'
    all_files = os.listdir(upload_folder_path)
    if not all_files:
        return 'No files uploaded'

    # get first file in upload folder
    target_file = all_files[0]
    full_file_path = os.path.join(upload_folder_path, target_file)

    # make sure target file is a text file
    if target_file[-4:] != '.txt':
        return ('Invalid file: ' + target_file)

    new_text = ''

    # run the letter replacer
    with open(full_file_path, 'rb') as infile:
        old_text = infile.read()
        new_text = delete_letter(old_text, 'a')

    # save the output
    download_folder_path = './data/output'
    full_download_path = os.path.join(download_folder_path, target_file)
    with open(full_download_path, 'wb') as outfile:
        outfile.write(new_text)

    return redirect(url_for('output_file', filename=target_file))


@myapp.route('/uploads/<filename>')
def uploaded_file(filename):
    folder_path = '../data/input'
    return send_from_directory(folder_path, filename)

@myapp.route('/outputs/<filename>')
def output_file(filename):
    folder_path = '../data/output'
    return send_from_directory(folder_path, filename)

@myapp.route('/download', methods=['GET'])
def download():
    pass
