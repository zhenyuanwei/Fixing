from flask import Flask

app = Flask(__name__)
app.secret_key = 'something is secret for others'

from app.views import flowview