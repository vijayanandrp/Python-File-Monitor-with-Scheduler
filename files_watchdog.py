#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

"""
   This script runs as a watchdog and scans for new files.
"""

import os
import pprint
import json
import time
import datetime as dt
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from lib.config import log_file, etc_path, input_path
from lib.logger import Logger
log = Logger.defaults(name="WATCH_DOG", logfile=log_file, output_stream=True, check_log_file=True)
from lib.util import OsUtils


__authors__ = ["P. Vijay Anand"]
__email__ = "vijayanandrp@gmail.com"
__version__ = "0.010"
__status__ = "This software is dedicated to our most honourable Chief Minister J.Jayalalitha Amma (1948-2016)"
__date__ = "05, Dec 2016"


def _json_to_dict(task_json):
    """ converts the json file into dictionary object """
    try:
        with open(task_json) as data_file:
            config_data = json.load(data_file)
    except (ValueError, FileNotFoundError, Exception):
        log.error("File reading error/ File may be opened for editing.", exc_info=True)
        return None
    log.debug("Task Json : \n %s" % pprint.pformat(config_data, indent=4))
    return config_data


def _get_config(task_json=None):
    """ module checks for the config file and converts the json to dict """
    task_json = os.path.join(etc_path, task_json)
    if not OsUtils().check_if_file_exist(task_json):
        log.error('Config.json - file not found')
        return None
    return _json_to_dict(task_json)


def get_config(task_json=None):
    """ Fetch Email Configurations values  for every schedule time """
    config_val = _get_config(task_json=task_json)
    if not config_val:
        return None
    return config_val
 
 
def schedule_time_calculator(**data):
    """ converts the schedule time to seconds  """
    schedule_time = dt.datetime.now() + dt.timedelta(data['days'], data['seconds'], data['microseconds'],
                                                     data['milliseconds'], data['minutes'], data['hours'], data['weeks'])
    date_string = schedule_time.strftime('%d-%m-%Y %H-%M-%S')
    new_date = schedule_time.strptime(date_string, '%d-%m-%Y %H-%M-%S')
    delay_seconds = (new_date - dt.datetime.now()).total_seconds()
    log.info('Seconds to get delay = {} secs.'.format(delay_seconds))
    return delay_seconds


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.*"]
    # patterns = ["*.msg", "*.eml"]
    
    @staticmethod
    def process(event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        file_name = str(event.src_path)
        log.info('Found -> {}'.format(file_name))
        
    def on_created(self, event):
        log.debug("Created - {}".format(bytes(event.src_path, "utf-8").decode('ascii', 'ignore')))
        self.process(event)

    def on_deleted(self, event):
        log.debug("Deleted - {}".format(bytes(event.src_path, "utf-8").decode('ascii', 'ignore')))
  

if __name__ == '__main__':
    log.info("#" * 77)
    log.info("#" * 20 + " | Files - WATCHDOG | -> Starts here " + "#" * 20)
    log.info("#" * 77)

    observer = Observer()
    observer.schedule(MyHandler(), path=input_path, recursive=True)
    observer.start()
    try:
        while True:
            config = get_config(task_json='config.json')
            if config:
                log.info('Valid Config.json .. Analyzing files status now... ')
                if config["is_schedule"]:
                    main_delay = schedule_time_calculator(**config["schedule_time"])
                    log.debug('Scheduling Enabled. Schedule Time in seconds - {} '.format(main_delay))
                    time.sleep(main_delay)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
 



