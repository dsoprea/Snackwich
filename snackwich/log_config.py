import logging

from getpass import getuser
from os import environ

if 'SNACKWICH_DEBUG' in environ and environ['SNACKWICH_DEBUG']:
    current_user = getuser()

    if current_user == 'root':
        log_filepath = 'snackwich.log'

    else:
        log_filepath = 'snackwich.log'

    logging.basicConfig(
            level       = logging.DEBUG,
            format      = '%(asctime)s  %(levelname)s %(message)s',
            filename    = log_filepath
        )

