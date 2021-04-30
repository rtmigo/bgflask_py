# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import pathlib
import sys
import os
from pathlib import Path
from typing import Optional, Dict, List

from bgprocess import BackgroundProcess


def get_by_case_insensitive_key(d: Dict[str, str], key: str) -> Optional[str]:
    key = key.upper()
    return next((v for (k, v) in d.items() if k.upper() == key), None)


def path_char():
    if isinstance(Path('.'), pathlib.WindowsPath):
        return ';'
    else:
        return ':'


class FlaskRunner:
    def __init__(self, command: List[str], add_env: Dict[str, str] = None,
                 start_timeout: float = 5.0):
        self.add_env = add_env
        self.command = command
        self.start_timeout = start_timeout
        self.server: Optional[BackgroundProcess] = None

    def __enter__(self):
        cmd = self.command.copy()
        if cmd and cmd[0] is None:
            cmd[0] = sys.executable

        # say, we run unittest with top_level_dir=project.
        #
        # So project/package/unit.py is normally importable as
        # "import package.unit".
        #
        # Now we run a child process "project/package/server.py". The
        # child interpreter sets sys.path[0] to "project/package". Since the
        # top level dir is not "project", we cannot "import package.unit"
        # anymore.
        #
        # We cannot stop interpreter from setting sys.path[0] to
        # "project/package". But we can suggest the look in "project" too.
        #
        # If user did not provide an exact PYTHONPATH variable for the
        # child process, we will it from the current sys.path.

        the_add_env = self.add_env or dict()
        pythonpath = get_by_case_insensitive_key(the_add_env, 'PYTHONPATH')
        if pythonpath is None:
            pythonpath = path_char().join(sys.path)
        the_add_env['PYTHONPATH'] = pythonpath

        self.server = BackgroundProcess(cmd, buffer_output=True,
                                        add_env=the_add_env)
        self.server.start()

        the_line = self.server.next_line(
            lambda line: line.startswith("* Running on http://127.0.0.1"),
            match_timeout=self.start_timeout)
        if the_line is None:
            raise RuntimeError(
                "Failed to start the server." + "\n".join(self.server.buffer))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.terminate()
