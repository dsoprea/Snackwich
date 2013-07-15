#!/usr/bin/python

from sys import exit

from snackwich.main import Snackwich

from config import config

panels = Snackwich(config)

result = panels.execute('window1')

if result is None:
    print("Cancelled.")
    exit(1)

from pprint import pprint
pprint(result)

