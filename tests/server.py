#!/usr/bin/env python3

# unit tests will run this file as an external process to check the terminal output and the HTTP responses
import os

#print("ENVIRON", os.environ)

from tests.import_me import FROM_IMPORT_ME

from flask import Flask

app = Flask(__name__)


@app.route('/say-hi')
def hi():
    return 'privet'


@app.route('/say-bye')
def bye():
    return 'poka'


@app.route('/imported1')
def imported1():
    return FROM_IMPORT_ME


@app.route('/get-x')
def x():
    return os.environ.get('my_test_x_variable') or ''


if __name__ == "__main__":
    app.run()
