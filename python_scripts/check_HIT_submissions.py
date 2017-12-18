import sys
from create_compensation_hit import get_client
from helper_functions import get_timestamp, get_log_directory
from pymongo import MongoClient

MAX_ASSIGNMENTS = 5

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
    print(len(hit_id_list))

    return hit_id_list

def check_submissions_MTurk(client, hit_id):

    hit = client.get_hit(HITId=hit_id)
    print 'MTurk status: {}'.format(hit['HIT']['HITStatus'])

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
            print(hit_id, HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)
            print(WorkerId, assignmentId, assignmentStatus)
    # Assignments complete
    else:
        print 'The assignments are fully Submitted: {}'.format(len(assignments))
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            MTurk_workers_assignments[WorkerId] = assignmentId

    return MTurk_workers_assignments

def check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments):
    print('hit collection:')
    hits_saved = hit_collection.find({'hitID':hit_id}).count()
    print(hits_saved)

    print('label collection:')
    for WorkerId in MTurk_workers_assignments.keys():
        labels_saved_per_worker = db.label.find({'hitID':hit_id, 'workerID':WorkerId}).count()
        print(WorkerId, labels_saved_per_worker)

if __name__ == '__main__':
    MTurk_client = get_client('production')

    MongoDB_client = MongoClient('localhost', 8081)
    db = MongoDB_client.meteor
    hit_collection = db['hit']
    label_collection = db['label']

    file_name = sys.argv[1]
    hit_id_list = read_HITs_log(file_name)

    for hit_id in hit_id_list:
        print(hit_id)
        MTurk_workers_assignments = check_submissions_MTurk(MTurk_client, hit_id)
        check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments)
        print