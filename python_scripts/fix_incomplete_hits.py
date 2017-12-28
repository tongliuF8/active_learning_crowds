import sys, re, os
from collections import defaultdict, OrderedDict
from pymongo import MongoClient
from tqdm import tqdm

from helper_functions import *
from insert_data_into_mongodb import get_data_path
from create_compensation_hit import get_client

HIT_COLLECTION = 'hit'
LABEL_COLLECTION = 'label'
MAX_ASSIGNMENTS_PERHIT = 5
SETS_OF_LABELS_PERHIT = 12

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

def check_submissions_MTurk(client, hit_id, MTurk_hits_assignments, MTurk_broken_hits):

    hit = client.get_hit(HITId=hit_id)
    HITStatus = hit['HIT']['HITStatus']
    HITCreationTime = hit['HIT']['CreationTime'].strftime("%Y-%m-%d %H:%M:%S")
    HITReviewStatus = hit['HIT']['HITReviewStatus']
    NumberOfAssignmentsPending = hit['HIT']['NumberOfAssignmentsPending']
    NumberOfAssignmentsAvailable = hit['HIT']['NumberOfAssignmentsAvailable']
    NumberOfAssignmentsCompleted = hit['HIT']['NumberOfAssignmentsCompleted']

    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.list_assignments_for_hit
    # Retrieve the results for a HIT
    response = client.list_assignments_for_hit(
        HITId=hit_id,
    )
    assignments = response['Assignments']

    #  Assignments lost
    if len(assignments) != MAX_ASSIGNMENTS_PERHIT:
        MTurk_broken_hits.append(hit_id)
        # print(hit_id, HITStatus, HITCreationTime, len(assignments), HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            assignmentStatus = assignment['AssignmentStatus']
            # print(WorkerId, assignmentId, assignmentStatus)
            MTurk_hits_assignments[hit_id].append((WorkerId, assignmentId))
    # Assignments complete
    else:
        # print 'The assignments are fully Submitted: {}'.format(len(assignments))
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            AcceptTime = assignment['AcceptTime']
            SubmitTime = assignment['SubmitTime']
            Duration = SubmitTime-AcceptTime
            # print(WorkerId, assignmentId, AcceptTime.strftime("%Y-%m-%d %H:%M:%S"), SubmitTime.strftime("%Y-%m-%d %H:%M:%S"), str(Duration))
            MTurk_hits_assignments[hit_id].append((WorkerId, assignmentId))

    return MTurk_hits_assignments, MTurk_broken_hits

def check_submissions_MongoDB(hit_collection, label_collection, MTurk_hits_assignments):

    MongoDB_hit_lost = defaultdict(int)

    for k, v in MTurk_hits_assignments.items():
        hit_id = k
        hits_saved = hit_collection.find({'hitID': hit_id}).count()
        if hits_saved != MAX_ASSIGNMENTS_PERHIT:
            MongoDB_hit_lost[hit_id] += 1
        # for item in v:
        #     WorkerId = item[0]
        #     worker_hit_saved = hit_collection.find({'hitID': hit_id, 'workerID': WorkerId}).count()
        #     if worker_hit_saved != 1:
        #         MongoDB_hit_lost[hit_id] += 1

    print('MongoDB hit_collection lost: %d' % len(MongoDB_hit_lost))
    for idx, k in enumerate(OrderedDict(sorted(MongoDB_hit_lost.items(), key=lambda k:k[1])).keys()):
        print(idx, k, MongoDB_hit_lost[k])

    hit_assignment_ids = defaultdict(set)
    MongoDB_label_lost = defaultdict(set)

    for k, v in MTurk_hits_assignments.items():
        hit_id = k
        for item in v:
            WorkerId = item[0]
            labels_saved_per_worker = label_collection.find({'hitID': hit_id, 'workerID': WorkerId}).count()
            if labels_saved_per_worker != SETS_OF_LABELS_PERHIT:
                MongoDB_label_lost[labels_saved_per_worker].add(hit_id)

        # else:
        #     labels = label_collection.find({'hitID': hit_id, 'workerID': WorkerId})
        #     for label in labels:
        #         MongoDB_assignmentID = label['assignmentID']
        #         if MTurk_assignmentId != MongoDB_assignmentID:
        #             print(hit_id, WorkerId, MTurk_assignmentId, MongoDB_assignmentID)
        #         else:
        #             hit_assignment_ids[hit_id].add(MTurk_assignmentId)


    print('MongoDB label_collection lost:')
    for k, v in OrderedDict(sorted(MongoDB_label_lost.items(), key=lambda k:k[0])).items():
        print(k, len(v), v)

    return hit_assignment_ids

def get_MTurk_hits_assignments(MTurk_client, hit_id_list):

    MTurk_hits_assignments = defaultdict(list)
    MTurk_broken_hits = []

    for hit_id in tqdm(hit_id_list):
        MTurk_hits_assignments, MTurk_broken_hits = check_submissions_MTurk(MTurk_client, hit_id, MTurk_hits_assignments, MTurk_broken_hits)

    print('MTurk broken HITs: %d' % len(MTurk_broken_hits))

    return MTurk_hits_assignments
            
if __name__ == '__main__':
    environment = sys.argv[1]
    timestamp_logs = read_hit_creation_log(environment)
    hit_id_list = read_HIT_logs(timestamp_logs)
    print(len(hit_id_list))

    MTurk_client = get_client(environment)
    print('MTurk API connected.')
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    hit_collection = db[HIT_COLLECTION]
    label_collection = db[LABEL_COLLECTION]
    print('MongoDB connected.')

    MTurk_hits_assignments = get_MTurk_hits_assignments(MTurk_client, hit_id_list)
    hit_assignment_ids = check_submissions_MongoDB(hit_collection, label_collection, MTurk_hits_assignments)
