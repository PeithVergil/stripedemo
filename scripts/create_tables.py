#!/usr/bin/env python

"""
A utility script that will automatically create all
tables defined by the models.

Usage:
    python scripts/create_tables.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stripedemo.core.models import database
from stripedemo.home.models import Customer
from stripedemo.session.models import Session


def main():
    with database:
        database.create_tables([
            Customer,
            Session,
        ])


if __name__ == '__main__':
    main()
