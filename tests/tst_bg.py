import os
import unittest
from pathlib import Path
import requests
from flaskrun import FlaskRunner

server_file_py = Path(__file__).parent / 'server.py'
command = [str(server_file_py)]


class TestFlaskBg(unittest.TestCase):

    def assert_not_running(self):
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://127.0.0.1:5000/say-hi')

    def assert_running(self):
        self.assertEqual(requests.get('http://127.0.0.1:5000/say-hi').text,
                         'privet')

    def test_first_arg_python3(self):
        self.assert_not_running()
        with FlaskRunner(['python3', str(server_file_py)]):
            self.assert_running()
        self.assert_not_running()

    def test_start_stop(self):
        # test the server is not running (yet)
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://127.0.0.1:5000/say-hi')

        # run server and get two different responses
        with FlaskRunner(command):
            self.assertEqual(requests.get('http://127.0.0.1:5000/say-hi').text,
                             'privet')
            self.assertEqual(requests.get('http://127.0.0.1:5000/say-bye').text,
                             'poka')

        # test the server is stopped
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get('http://127.0.0.1:5000/say-hi')

    def test_env(self):
        assert os.environ.get('my_test_x_variable') is None

        with FlaskRunner(command):
            self.assertEqual(requests.get('http://127.0.0.1:5000/get-x').text,
                             '')

        with FlaskRunner(command, add_env={'my_test_x_variable': '42'}):
            self.assertEqual(requests.get('http://127.0.0.1:5000/get-x').text,
                             '42')

        # we did not change the environment: the variable was passed to particular Flask instance,
        # so if we start again, the variable is not defined
        with FlaskRunner(command):
            self.assertEqual(requests.get('http://127.0.0.1:5000/get-x').text,
                             '')


if __name__ == "__main__":
    TestFlaskBg().test_env()
