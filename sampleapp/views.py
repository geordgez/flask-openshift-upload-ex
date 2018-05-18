from sampleapp import myapp

@myapp.route('/')
def helloworld():
    return 'Hello World!'

@myapp.route('/upload', methods=['GET', 'POST'])
def upload():
    pass

@myapp.route('/download', methods=['GET'])
def download():
    pass
