import sys, pprint
from create_compensation_hit import get_client
from helper_functions import get_timestamp, get_log_directory
from pymongo import MongoClient
from collections import OrderedDict

MAX_ASSIGNMENTS = 5
SETS_OF_LABELS = 12

def read_HITs_log(file_name):

    hit_id_list = list()
    with open(get_log_directory('HITs') + "/" + file_name) as input_file:
        line_number = 0
        for line in input_file:
            line_number += 1
            validation = line.strip().split(":")[0]
            if line_number % 2 == 1 and validation == "Your HIT ID is":
                hit_id = line.strip().split(":")[1]
                hit_id_list.append(hit_id.strip())

    return hit_id_list

def check_submissions_MTurk(client, hit_id):

    print('MTurk API report:')

    hit = client.get_hit(HITId=hit_id)
    print 'HIT status: {}'.format(hit['HIT']['HITStatus'])

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

    MTurk_workers_assignments = {}

    #  Assignments lost
    if len(assignments) != MAX_ASSIGNMENTS:
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            assignmentStatus = assignment['AssignmentStatus']
            print(WorkerId, assignmentId, assignmentStatus)
            MTurk_workers_assignments[WorkerId] = assignmentId
        print(hit_id, len(assignments), HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)
    # Assignments complete
    else:
        print 'The assignments are fully Submitted: {}'.format(len(assignments))
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            print(assignment.keys())
            MTurk_workers_assignments[WorkerId] = assignmentId

    return MTurk_workers_assignments

def check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments):

    print('MongoDB report:')

    print('hit collection:')
    hits_saved = hit_collection.find({'hitID':hit_id}).count()
    print(hits_saved)

    print('label collection:')

    for WorkerId in MTurk_workers_assignments.keys():
        labels_saved_per_worker = label_collection.find({'hitID': hit_id, 'workerID': WorkerId}).count()
        print(WorkerId, labels_saved_per_worker, SETS_OF_LABELS)

        if labels_saved_per_worker != SETS_OF_LABELS:
            _ids = []
            assignmentIds = []
            id_s = []
            assignment_timestamp = {}

            for record in label_collection.find({'hitID': hit_id, 'workerID': WorkerId}):
                _id = record['_id']
                _ids.append(_id)
                assignmentId = record['assignmentID']
                assignmentIds.append(assignmentId)
                id_ = record['id']
                id_s.append(id_)
                timestamp = record['timestamp']
                assignment_timestamp[_id] = timestamp

            print('_id', len(_ids), len(set(_ids)))
            print('assignmentID', len(assignmentIds), len(set(assignmentIds)))
            print('id', len(id_s), len(set(id_s)))
            for k, v in OrderedDict(sorted(assignment_timestamp.items(), key=lambda p: p[1])).items():
                print(k, v)

if __name__ == '__main__':
    MTurk_client = get_client('production')

    print('Account balance:')
    print(MTurk_client.get_account_balance())

    MongoDB_client = MongoClient('localhost', 8081)
    db = MongoDB_client.meteor
    hit_collection = db['hit']
    label_collection = db['label']

    file_name = sys.argv[1]
    hit_id_list = read_HITs_log(file_name)
    print 'Checking {} HITs......\n'.format(len(hit_id_list))

    for index, hit_id in enumerate(hit_id_list):
        print(index, hit_id)
        MTurk_workers_assignments = check_submissions_MTurk(MTurk_client, hit_id)
        print
        check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments)
        print