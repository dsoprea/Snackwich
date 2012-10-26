#!/usr/bin/python

from snackwich.snackwich import Snackwich

panels = Snackwich('example.snack.py')

result = panels.execute()

from pprint import pprint
pprint(result)

