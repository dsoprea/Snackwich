
from snackwich import Snackwich

panels = Snackwich('example.snack.py')

from pprint import pprint
pprint(panels.execute())

