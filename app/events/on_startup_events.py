"""
Containing events to handle on app startup
"""

import datetime


def startup_events():
    datetime_str = str(datetime.datetime.now())
    print(f'App startup [{datetime_str}]')
