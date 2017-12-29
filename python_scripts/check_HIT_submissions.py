import sys
from create_compensation_hit import get_client
from helper_functions import get_timestamp, get_log_directory
from pymongo import MongoClient
from collections import defaultdict, OrderedDict

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

    MTurk_workers_assignments = {}

    #  Assignments lost
    if len(assignments) != MAX_ASSIGNMENTS:
        print(hit_id, len(assignments), HITCreationTime, HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            assignmentStatus = assignment['AssignmentStatus']
            print(WorkerId, assignmentId, assignmentStatus)
            MTurk_workers_assignments[WorkerId] = assignmentId
    # Assignments complete
    else:
        print 'The assignments are fully Submitted: {}'.format(len(assignments))
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            AcceptTime = assignment['AcceptTime']
            SubmitTime = assignment['SubmitTime']
            Duration = SubmitTime-AcceptTime
            print(WorkerId, AcceptTime.strftime("%Y-%m-%d %H:%M:%S"), SubmitTime.strftime("%Y-%m-%d %H:%M:%S"), str(Duration))
            MTurk_workers_assignments[WorkerId] = assignmentId

    return MTurk_workers_assignments

def check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments):

    print('MongoDB report:')

    print('hit collection:')
    hits_saved = hit_collection.find({'hitID': hit_id}).count()
    print(hits_saved)
    for WorkerId in MTurk_workers_assignments.keys():
        worker_hits_saved = hit_collection.find({'hitID': hit_id, 'workerID': WorkerId}).count()
        print(WorkerId, worker_hits_saved)

    print('label collection:')

    hit_assignment_ids = defaultdict(set)

    for WorkerId, MTurk_assignmentId in MTurk_workers_assignments.items():
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
                print(k, v.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            labels = label_collection.find({'hitID': hit_id, 'workerID': WorkerId})
            for label in labels:
                MongoDB_assignmentID = label['assignmentID']
                if MTurk_assignmentId != MongoDB_assignmentID:
                    print(hit_id, WorkerId, MTurk_assignmentId, MongoDB_assignmentID)
                else:
                    hit_assignment_ids[hit_id].add(MTurk_assignmentId)

    return hit_assignment_ids

if __name__ == '__main__':
    MTurk_client = get_client('production')

    print('Account balance: {}'.format(MTurk_client.get_account_balance()['AvailableBalance']))

    MongoDB_client = MongoClient('localhost', 8081)
    db = MongoDB_client.meteor
    hit_collection = db['hit']
    label_collection = db['label']

    user_input = sys.argv[1]
    # Get hit id(s) from log file (.txt)
    if user_input.endswith('.txt'):
        file_name = user_input
        hit_id_list = read_HITs_log(file_name)
        print 'Checking {} HITs......\n'.format(len(hit_id_list))

        for index, hit_id in enumerate(hit_id_list):
            print(index, hit_id)
            MTurk_workers_assignments = check_submissions_MTurk(MTurk_client, hit_id)
            print
            hit_assignment_ids = check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments)
            print
    # Get hid id from command line
    else:
        hit_id = user_input
        print 'Checking HIT {}...\n'.format(hit_id)
        MTurk_workers_assignments = check_submissions_MTurk(MTurk_client, hit_id)
        print
        hit_assignment_ids = check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments)
        print