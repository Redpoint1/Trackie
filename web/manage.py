#!/usr/bin/env python

""" Django manage """

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_PROJECT_ROOT",
                          os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trackie.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
