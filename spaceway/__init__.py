from sys import version_info

MIN_PYTHON = (3, 7, 0)

if version_info < MIN_PYTHON:
    raise Exception('Space Way requires Python {0}.{1}.{2} or newer'.format(*MIN_PYTHON))

from . import main  # noqa: F401,E402
