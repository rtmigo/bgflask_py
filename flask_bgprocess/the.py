# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import unittest
from typing import Optional, Dict, List

from bgprocess import BackgroundProcess


class FlaskBackground:
    def __init__(self, command: List[str], add_env: Dict[str, str] = None, start_timeout: float = 5.0):
        self.add_env = add_env
        self.command = command
        self.start_timeout = start_timeout
        self.server: Optional[BackgroundProcess] = None

    def __enter__(self):
        self.server = BackgroundProcess(self.command, buffer_output=True, add_env=self.add_env)
        self.server.start()

        the_line = self.server.next_line(lambda line: line.startswith("* Running on http://127.0.0.1"),
                                         match_timeout=self.start_timeout)
        if the_line is None:
            raise RuntimeError("Failed to start the server." + "\n".join(self.server.buffer))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.terminate()


