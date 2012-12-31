#!/usr/bin/python
import os
from contextlib import contextmanager

@contextmanager
def suppress_output(fd):
    if hasattr(fd, 'fileno'):
        if hasattr(fd, 'flush'):
            fd.flush()
        fd = fd.fileno()
    oldfd = os.dup(fd)
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        try:
            os.dup2(devnull, fd)
        finally:
            os.close(devnull)
        yield
        os.dup2(oldfd, fd)
    finally:
        os.close(oldfd)
#import sys

#with suppress_output(sys.stderr):
    #import gtk