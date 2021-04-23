Python package running local Flask server process in the background.

Tested on Linux and macOS with Python 3.7-3.9.

---
# Why

I prefer to test the server like a black box, accessing only the HTTP API it provides.

Also, I want the same code to test my application, whether it is running locally or on the server.

``` python
test_my_app('http://127.0.0.1:5000')  # test Flask running locally
test_my_app('http://remote-service-api.com')  # test the same app deployed
```

I could manually start the local Flask server in a terminal window and get a working 
API at 127.0.0.1:5000. But I don't want to do anything manually: neither launch a 
terminal, nor a command in it. This should be done automatically by the testing code.

# What it does

The library provides the `FlaskBackground` class. 

The `FlaskBackground` starts the local Flask server in parallel process.

The same effect could be achieved by simply launching standard Flask application in a terminal window:

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

The `FlaskBackground` does the same silently, without additional terminal window.

``` python
with FlaskBackground(['python3', '/my/flask-app/main.py']):
  # Running on http://127.0.0.1:5000/
  # No need for Ctrl+C. Get out of `with` and the server stops
```

# How to Install

``` bash
$ pip install git+https://github.com/rtmigo/bgflask_py#egg=bgflask
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
from bgprocess import FlaskBackground

# the server is not running  

with FlaskBackground(["python3", "/path/to/main.py"]):

    # we have just started "python3 /path/to/main.py"
        
    # So the server is running, and you can send requests 
    # directly to localhost. By default the Flask server listens  
    # to port 5000
    
    assert requests.get('http://127.0.0.1:5000/status') == 'OK'
    assert requests.get('http://127.0.0.1:5000/answer') == '42'
    
# the server is not running again     
```
