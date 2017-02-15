#!/usr/bin/env python

import sys
import os.path
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from django.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
