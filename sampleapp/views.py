from sampleapp import myapp

from flask import render_template

@myapp.route('/')
def helloworld():
    return 'Hello World!'

@myapp.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@myapp.route('/download', methods=['GET'])
def download():
    pass
