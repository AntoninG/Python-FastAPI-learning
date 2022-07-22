"""
Containing events to handle on app shutdown
"""

import datetime


def shutdown_print():
    datetime_str = str(datetime.datetime.now())
    print(f'App shutdown [{datetime_str}]')
