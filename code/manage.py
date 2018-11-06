#!/usr/bin/env python -W ignore
from __future__ import unicode_literals, absolute_import
import os
import subprocess
import sys

from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))

VE_ROOT = path.join(PROJECT_ROOT, '../env')
VE_ACTIVATE = path.join(VE_ROOT, 'bin', 'activate_this.py')


# Convinience method to activate env
def go_to_ve():
    # going into ve
    if not VE_ROOT in sys.prefix:
        if sys.platform == 'win32':
            python = path.join(VE_ROOT, 'Scripts', 'python.exe')
        else:
            python = path.join(VE_ROOT, 'bin', 'python')
        try:
            retcode = subprocess.call([python, __file__] + sys.argv[1:])
        except KeyboardInterrupt:
            retcode = 1
        sys.exit(retcode)

#go_to_ve()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
