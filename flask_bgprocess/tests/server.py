#!/usr/bin/env python3

# unit tests will run this file as an external process to check the terminal output and the HTTP responses
import os

from flask import Flask

app = Flask(__name__)


@app.route('/say-hi')
def hi():
    return 'privet'


@app.route('/say-bye')
def bye():
    return 'poka'


@app.route('/get-x')
def x():
    return os.environ.get('my_test_x_variable') or ''


if __name__ == "__main__":
    app.run()
