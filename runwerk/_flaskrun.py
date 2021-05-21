# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import os
import warnings
import pathlib
import sys
from pathlib import Path
from typing import Optional, Dict, List

from bgprocess import BackgroundProcess


def get_by_case_insensitive_key(d: Dict[str, str], key: str) -> Optional[str]:
    # todo unit test
    key = key.upper()
    values = set(v for (k, v) in d.items() if k.upper() == key)
    if len(values) >= 2:
        raise ValueError("More than one item found by the case-insensitive key")
    if values:
        return next(iter(values))
    else:
        return None


def path_char():
    """The character placed between parts of $PATH and $PYTHONPATH environment
    variable"""
    if isinstance(Path('.'), pathlib.WindowsPath):
        return ';'
    else:
        return ':'


def env_enabled():
    if os.getenv('FLASKRUN') is not None:
        # outdated since 2021-05
        warnings.warn('Use RUNWERK_ENABLED environment var instead of FLASKRUN')

    for var in ['FLASKRUN', 'RUNWERK_ENABLED']:
        value = os.getenv(var) or '1'
        value = value.strip().lower()
        if value == '0' or value == "false":
            return False
        if value != '1' and value != 'true':
            warnings.warn(f'Unexpected {var} value: "{value}"')
    return True


class RunWerk:
    def __init__(self,
                 command: List[str] = None,
                 module: str = None,
                 add_env: Dict[str, str] = None,
                 start_timeout: float = 5.0,
                 copy_pythonpath: bool = True):
        """

        :param command: The command to run the server. For example,
        ['python3', 'my_server.py']. If the first item it None, it will be
        replaced with the current Python executable: [None, 'my_server.py'].

        :param module: A shorter alternative to [command] in case the command
        is just [python3 -m pkg.module].

        :param add_env:
        :param start_timeout:
        :param copy_pythonpath:
        """

        if (command is None) == (module is None):
            raise ValueError("Please specify either `module` or `command`, "
                             "but not both.")

        self.add_env = dict() if add_env is None else add_env.copy()
        self.command = command
        self.module = module
        self.start_timeout = start_timeout
        self.server: Optional[BackgroundProcess] = None
        self.copy_pythonpath = copy_pythonpath

    def _pythonpath_to_add_env(self):

        # say, we're running unittest with top_level_dir=project.
        #
        # So project/package/unit.py is importable as "import package.unit".
        #
        # From the test we start a child process "project/package/server.py".
        # The child interpreter sets sys.path[0] to "project/package". Since
        # the top level dir is not "project" for the child, it cannot
        # "import package.unit".
        #
        # We cannot stop child interpreter from setting sys.path[0] to
        # "project/package". But we can suggest it to look in "project" too.
        #
        # If user did not provide an exact PYTHONPATH variable for the
        # child process, we will create it from the current sys.path.

        assert self.copy_pythonpath

        pythonpath = get_by_case_insensitive_key(self.add_env, 'PYTHONPATH')
        if pythonpath is None:
            pythonpath = path_char().join(sys.path)
        self.add_env['PYTHONPATH'] = pythonpath

    def _gen_args(self) -> List[str]:

        if self.command is not None:
            cmd = self.command.copy()
            if cmd and cmd[0] is None:
                cmd[0] = sys.executable
            return cmd
        else:
            assert self.module is not None
            return [sys.executable, "-m", self.module]

    def __enter__(self):

        if not env_enabled():
            return

        if self.copy_pythonpath:
            self._pythonpath_to_add_env()

        self.server = BackgroundProcess(self._gen_args(),
                                        buffer_output=True,
                                        add_env=self.add_env)
        self.server.start()

        the_line = self.server.next_line(
            lambda line: line.startswith("* Running on http://127.0.0.1"),
            match_timeout=self.start_timeout)
        if the_line is None:
            raise RuntimeError(
                "Failed to start the server." + "\n".join(self.server.buffer))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server is not None:
            self.server.terminate()
            self.server = None
