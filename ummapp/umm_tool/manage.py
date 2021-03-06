#!/usr/bin/env python
import os
import os.path
import sys

sys.path.insert(0, os.path.join(os.pardir, 'lib'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "umm_tool.settings")

    from djangae.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
