# Additional extensions

# Django imports
from django.db import connections
from django.db.utils import OperationalError
# Python imports

# Third party imports


def check_default_database_connection():
    
    try:
        my_conn = connections['default']
        cursor = my_conn.cursor()
    except OperationalError as e:
        print(e)
        connectied = False
    else:
        connected = True

    return connected
