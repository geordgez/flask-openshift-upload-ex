from flask import Flask

myapp = Flask(__name__)

from sampleapp import views
from sampleapp.scripts import delete_letter

myapp.secret_key = 'my_special_sauce'
