import os
from datetime import datetime, timedelta
from lib.logger import Logger


class DateTime(object):

    def __init__(self):
        self.log = Logger.defaults(name="DateTime", output_stream=False)
    
    def get_date_time(self, fmt='%Y-%m-%d-%H-%M-%S'):
        date_stamp = datetime.now().strftime(fmt)
        self.log.debug("date_stamp_with_time: %s " % date_stamp)
        return date_stamp
    
    def get_date(self, fmt='%Y-%m-%d'):
        date_stamp = datetime.now().strftime(fmt)
        self.log.debug("date_stamp_date_only: %s " % date_stamp)
        return date_stamp
    
    def get_time(self, fmt='%H-%M-%S'):
        date_stamp = datetime.now().strftime(fmt)
        self.log.debug("date_stamp_time_only: %s " % date_stamp)
        return date_stamp
    
    def get_date_with_subtract(self, fmt='%Y-%m-%d', days_to_subtract=1):
        date_stamp = datetime.now() + timedelta(days=-days_to_subtract)
        date_stamp = date_stamp.strftime(fmt)
        self.log.debug("date_stamp_with_days_subtraction: %s " % date_stamp)
        return date_stamp


class OsUtils(object):
    def __init__(self):
        self.log = Logger.defaults(name="OsUtils", output_stream=False)

    def check_if_file_exist(self, file_name=None):
        if not file_name:
            self.log.warning("file is empty")
            return False
        if os.path.isfile(file_name):
            self.log.info("file {} is found".format(file_name))
            return True
        else:
            self.log.info("file ({} not found".format(file_name))
            return False

    def fetch_files_from_path(self, path=None):
        if not path:
            self.log.info('Path cannot be None')
            return False
        if not os.path.isdir(path):
            self.log.info('Path is not valid')
            return False
        for path, dirs, files in os.walk(path):
            return files
