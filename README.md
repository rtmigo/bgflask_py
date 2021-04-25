# [flaskrun](https://github.com/rtmigo/flaskrun_py#flaskrun)

Python package running local Flask server process in the background.

Tested on Linux and macOS with Python 3.7-3.9.

---

# Why

I prefer to **test** my own **Flask server** like a **black box**. I want to
access only the public HTTP API the server provides. So I can test both local
and remote servers the same way.

``` python
test_my_api('http://127.0.0.1:5000')
test_my_api('http://deployed-on-remote-server.net')
```

I also want to start and restart the local testing server easily. So I'll be
sure, that no variables are cached between requests: not only the `Flask` object
reset, but the whole Python process with the API was restarted.

I could *manually* start the local Flask server in a terminal window and get a
working API at 127.0.0.1:5000. But I want this to be done *automatically*, since
the tests are automated.

# FlaskRunner

The `FlaskRunner` object starts the local Flask server in parallel process and
keeps it running.

The same effect could be achieved by launching standard Flask application in a
terminal:

``` bash
$ python3 /my/flask-app/main.py
```

``` text
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The `FlaskRunner` does the same silently, without terminal window.

``` python
with FlaskRunner(['python3', '/my/flask-app/main.py']):
  # the server was started and initialized.
  # It is now running on http://127.0.0.1:5000/
  # No need for Ctrl+C. Get out of `with` and the server stops
  pass
```

# How to Install

``` bash
$ pip install git+https://github.com/rtmigo/flaskrun_py#egg=flaskrun
```

# How to Use

We assume, your `main.py` contains something like

``` python3
from flask import Flask

app = Flask(__name__)

@app.route('/status')
def status():
    return 'OK'
    
@app.route('/answer')
def answer():
    return '42'
    
if __name__ == "__main__":
    app.run()
```

Then you can run tests like this:

``` python3
import requests
from flaskrun import FlaskRunner

# the server is not running  

with FlaskRunner(["python3", "/path/to/main.py"]):

    # we have just started "python3 /path/to/main.py"
        
    # So the server is running, and you can send requests 
    # directly to localhost. By default the Flask server listens  
    # to port 5000
    
    assert requests.get('http://127.0.0.1:5000/status') == 'OK'
    assert requests.get('http://127.0.0.1:5000/answer') == '42'
    
# the server is not running again     
```
