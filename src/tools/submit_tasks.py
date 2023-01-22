"""
BackgroundTasks
"""

# import libraries
from datetime import date, datetime
from decouple import config
import os

async def write_notification(metadata: str, message=""):
    """
    This function will keep the calling requests
    """
    # log type could be access or error
    # # # Values Definitions # # # 
    machine_root_directory = os.path.abspath(os.curdir)

    today = str(date.today())
    now = str(datetime.now())

    txt_fullname = machine_root_directory + '/trace/' + today + '_' + '.log'

    with open(txt_fullname, mode="a", encoding='utf-8') as f:
        f.write(now + ' | ' + metadata + ' | ' +  message + '\n')
        f.close()
