from flask import Flask
app = Flask(__name__)
from setlistapp import views
# The views are the handlers that respond to requests from
# web browsers. In Flask views are written as Python functions.
# Each view function is mapped to one or more request URLs.
