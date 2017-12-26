import time, os
from insert_data_into_mongodb import get_data_path

def get_timestamp():

    return time.strftime("%Y%m%d_%H%M%S")

def get_log_directory(logtype):

    log_dir = get_data_path() + '/'+ logtype + '/'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    return log_dir

def datetime2string(datetime):
    
    return datetime.strftime("%Y-%m-%d %H:%M:%S")