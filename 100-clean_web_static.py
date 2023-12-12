#!/usr/bin/python3
import os
from fabric.api import *

env.hosts = ['100.25.179.31', '54.237.87.213']


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)
    number = 1 if number < 1 else number

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        archives_to_delete = local_archives[:-number]
        [local("rm -f {}".format(a)) for a in archives_to_delete]

    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr | grep web_static").split()
        archives_to_delete = remote_archives[:-number]
        [sudo("rm -rf {}".format(a)) for a in archives_to_delete]
