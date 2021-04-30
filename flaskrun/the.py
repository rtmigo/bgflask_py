# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT
import sys, os
from typing import Optional, Dict, List

from bgprocess import BackgroundProcess


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



        self.server = BackgroundProcess(cmd, buffer_output=True,
                                        add_env=self.add_env,
                                        #add_env={"PYTHONPATH": os.path.abspath('.')+":"+(os.environ.get("PYTHONPATH") or '')},
                                        #cwd=os.path.abspath('.')
                                        )
        self.server.start()

        the_line = self.server.next_line(
            lambda line: line.startswith("* Running on http://127.0.0.1"),
            match_timeout=self.start_timeout)
        if the_line is None:
            raise RuntimeError(
                "Failed to start the server." + "\n".join(self.server.buffer))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.terminate()
