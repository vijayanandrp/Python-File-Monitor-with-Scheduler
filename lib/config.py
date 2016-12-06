import os

# get root directory
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# File Name
config = 'config.json'
log = 'watchdog.log'

# directory configurations
data_path = os.path.join(root_dir, 'data')         # data
input_path = os.path.join(data_path, 'input')      # data/input
log_path = os.path.join(data_path, 'log')          # data/log
# logger configurations
log_file = os.path.join(log_path, log)
etc_path = os.path.join(data_path, 'etc')          # etc
job_json = os.path.join(etc_path, config)          # etc/config.json



