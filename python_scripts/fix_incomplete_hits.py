import sys, re, os
from helper_functions import *
from insert_data_into_mongodb import get_data_path
from check_HIT_submissions import *
from pymongo import MongoClient

HIT_COLLECTION = 'hit'
LABEL_COLLECTION = 'label'

def read_hit_creation_log(environment):

    timestamp_logs = []
    
    if environment == 'production':
        log_file_path = get_log_directory("HITcreation") +"/tweet_usage_log"
    else:
        log_file_path = get_log_directory("HITcreation") + "/sandbox_CFtweet_usage_log"

    pattern = re.compile(r'^(timestamp:)(\w+)')

    with open(log_file_path) as logfile:
        for line in logfile:
            string = line.strip("\n")
            timestamp = re.search(pattern, string).groups()[1]
            timestamp_digit = timestamp.replace('_', '')
            timestamp_logs.append(timestamp_digit)

    return timestamp_logs

def read_HIT_logs(timestamp_logs):

    file_names = ['20171212_222529.txt', '20171213_214953.txt', '20171214_025235.txt', '20171214_032438.txt', '20171214_040225.txt', '20171214_144105.txt', '20171215_210716.txt', '20171216_210643.txt', '20171217_151734.txt', '20171218_025606.txt', '20171220_030205.txt', '20171220_220434.txt', '20171221_030115.txt', '20171221_145931.txt', '20171222_145844.txt', '20171222_215518.txt', '20171223_030245.txt', '20171223_185409.txt', '20171224_023912.txt', '20171224_073200.txt', '20171224_201913.txt', '20171225_043948.txt', '20171225_185223.txt', '20171226_020804.txt', '20171226_152744.txt', '20171226_195320.txt', '20171226_234948.txt', '20171227_020642.txt', '20171227_045935.txt', '20171227_164932.txt', '20171227_181131.txt', '20171227_194256.txt']

    print(len(timestamp_logs), len(file_names), len(timestamp_logs) == len(file_names))

    hit_id_list = []

    for file_name in file_names:
        with open(get_log_directory('HITs') + "/" + file_name) as input_file:
            line_number = 0
            for line in input_file:
                line_number += 1
                validation = line.strip().split(":")[0]
                if line_number % 2 == 1 and validation == "Your HIT ID is":
                    hit_id = line.strip().split(":")[1]
                    hit_id_list.append(hit_id.strip())

    return hit_id_list
            
if __name__ == '__main__':
    environment = sys.argv[1]
    timestamp_logs = read_hit_creation_log(environment)
    hit_id_list = read_HIT_logs(timestamp_logs)
    print(len(hit_id_list))

    MTurk_client = get_client('production')
    print('MTurk API connected\n')
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    hit_collection = db[HIT_COLLECTION]
    label_collection = db[LABEL_COLLECTION]
    print('MongoDB connected\n')

    for index, hit_id in enumerate(hit_id_list):
        print(index, hit_id)
        MTurk_workers_assignments = check_submissions_MTurk(MTurk_client, hit_id)
        print
        hit_assignment_ids = check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments)
        print
