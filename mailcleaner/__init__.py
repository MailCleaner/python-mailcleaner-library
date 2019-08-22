#!/usr/bin/env python3
"""
    MailCleaner Python API
    ~~~~~~~~~~~~~~~~~~~~~~

    This package is a high level API for interacting with MailCleaner core components such as databases, dumpers etc.

    :copyright: (c) 2019 by the MailCleaner Team.
    :license: GNU GENERAL PUBLIC LICENSE, see LICENSE for more details.

"""

__docformat__ = 'restructuredtext en'
__version__ = '0.1'


from .dumper import *
from .db import *
from .db.models import *
from .db.config import *
from .config import *