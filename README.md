# [runwerk](https://github.com/rtmigo/runwerk_py#readme)

Python package running child Werkzeug server process in the background.

This allows you to launch a web application and send a request to it.

``` python3
with RunWerk(module="myapp.main"):
    response = requests.get('http://127.0.0.1:5000/hi')
```


This is useful for testing web applications. In particular, Flask applications.

Runwerk supports Python 3.7+ on Linux and macOS.

--------------------------------------------------------------------------------

I prefer to **test** my own **Flask app** like a **black box**. I want to access
only the public HTTP API the server provides. So I can test both local and
remote servers the same way.

``` python
test_my_api('http://127.0.0.1:5000')
test_my_api('http://deployed-on-remote-server.net')
```

I also want to easily restart the local server process. This way, I can be sure
that after a restart, the global variables inside the server have their default
values.

I could *manually* start the local Flask+Werkzeug server in a terminal window
and get a working API at 127.0.0.1:5000. But I want this to be done *
automatically*, since the tests are automated.

The `RunWerk` object starts the local server in parallel process and keeps it
running.

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

The `RunWerk` does the same silently, without terminal window.

``` python
with RunWerk(command=['python3', '/path/flask_app/main.py']):
  # the server was started and initialized.
  # It is now running on http://127.0.0.1:5000/
  # No need for Ctrl+C. Get out of `with` and the server stops
  pass
```

# Install

``` bash
$ pip install git+https://github.com/rtmigo/runwerk_py#egg=runwerk
```

# Use

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
from runwerk import RunWerk

# the server is not running  

with RunWerk(["python3", "/path_to/flask_app/main.py"]):

    # we have just started main.py
        
    # So the server is running, and you can send requests 
    # directly to localhost. By default the Flask server listens  
    # to port 5000
    
    assert requests.get('http://127.0.0.1:5000/status') == 'OK'
    assert requests.get('http://127.0.0.1:5000/answer') == '42'
    
# the server is not running again     
```

## Creating RunWerk

### With module name

``` python3 
with RunWerk(module="main"):
    pass
```

``` python3 
with RunWerk(module="flask_app.main"):
    pass
```

### With command line

``` python3 
with RunWerk(["python3", "/path_to/flask_app/main.py"]):
    pass
```

To run command with the current interpreter (`sys.executable`), you can set the
first item of `command` to `None`.

``` python3 
with RunWerk([None, "/path_to/flask_app/main.py"]):
    pass
```

## Temporary disabling RunWerk

When `$RUNWERK_ENABLED` environment variable is set to `False`, the server will
not be started. The code runs as usual, but `RunWerk` object does nothing.

``` bash
RUNWERK_ENABLED=False python3 run_my_unittest.py
```

This is useful when you're running the server manually, for example, when
debugging.
