# -*- coding: utf-8 -*-
import os
from lib.config import log_file, log_path
from datetime import datetime, timedelta
import inspect
import logging
import traceback


def get_func_name():
    return '\tFunction Name: {}'.format(traceback.extract_stack(None, 2)[0][2])


def get_func_params():
    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    return '\tFunction Name: {} - Params - {}'.format(traceback.extract_stack(None, 2)[0][2],
                                                      str([(i, values[i]) for i in args]))


def date_stamp_with_days_subtraction(fmt='%Y-%m-%d', days_to_subtract=1):
    date_stamp = datetime.now() + timedelta(days=-days_to_subtract)
    date_stamp = date_stamp.strftime(fmt)
    return date_stamp


class Logger(object):
    """ module for logging the executions and statements """

    @staticmethod
    def defaults(name, logfile=log_file, debug_level='DEBUG', output_stream=True, check_log_file=False):
        """ default configuration settings in the method """
        
        if check_log_file:
            """ Backup the old log file with date stamp """
            new_file = "{}_{}".format(date_stamp_with_days_subtraction(days_to_subtract=1), os.path.basename(logfile))
            new_file = os.path.join(log_path, new_file)
            print(new_file, log_file)
            if not os.path.isfile(new_file):
                os.rename(log_file, new_file)
        
        if debug_level is "INFO":
            debug_level = logging.INFO
        elif debug_level is "DEBUG":
            debug_level = logging.DEBUG
        else:
            debug_level = logging.INFO

        # log file configuration
        logging.basicConfig(
            level=debug_level,
            filename=logfile,
            filemode='a',
            format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d/%b/%Y %H:%M:%S')

        if type(output_stream) is bool and output_stream:
            # console output
            console = logging.StreamHandler()
            console.setLevel(debug_level)
            console.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
            logging.getLogger('').addHandler(console)

        return logging.getLogger("{}".format(name))



