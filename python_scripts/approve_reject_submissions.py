import sys
from collections import defaultdict
from pymongo import MongoClient
from helper_functions import *
from check_HIT_submissions import *

HIT_COLLECTION = 'hit'
LABEL_COLLECTION = 'label'

# check answers for duplicated tweets

def validate_q12(answer1, answer2):

    if (answer1['question1'] == answer2['question1']) and (answer1['question2'] == answer2['question2']):
        return True


def validate_q3(answer1, answer2):

    q3_result1 = answer1['question3']
    q3_result2 = answer2['question3']
    q1_set = set()
    q2_set = set()
    for i in range(len(q3_result1)):
        if q3_result1[i]['checked'] == 1:
            q1_set.add(q3_result1[i]['option'])
        if q3_result2[i]['checked'] == 1:
            q2_set.add(q3_result2[i]['option'])

    if len(q1_set - q2_set) < 2:
        return True
    else:
        return False


def check_database_records(hit_id_list, hit_collection, label_collection):

    hit_assignment_ids = defaultdict(list)

    for index, hit_id in enumerate(hit_id_list):
        for document in hit_collection.find({'hitID': hit_id}):
            # document.keys(): [u'assignmentID', u'workerID', u'tweetList', u'_id', u'hitID']
            assignment_id = document['assignmentID']
            worker_id = document['workerID']
            tweet_id_list = document['tweetList']
            _id = document['_id']
            hit_assignment_ids[hit_id].append(assignment_id)

            # tweet_id_set = set()
            # match_count = 0
            # mismatch = 0

            labels_list = []

            for tweet_id in tweet_id_list:
                # if mismatch > 0:
                #     print("Reject assignment (HITID:{} AssignmentID:{} workerID: {})".format(hit_id, assignment_id,
                #                                                                             worker_id))
                #     break
                result = label_collection.find({'hitID': hit_id, 'workerID': worker_id, 'assignmentID': assignment_id, 'id': tweet_id})
                labels_list.append(result)

            #     if result.count() == 2 and tweet_id not in tweet_id_set:
            #         if validate_q12(result[0], result[1]):
            #             if validate_q3(result[0], result[1]):
            #                 match_count += 1
            #             else:
            #                 mismatch += 1
            #         else:
            #             mismatch += 1

            #     tweet_id_set.add(tweet_id)
            # if mismatch == 0:
            #     print("Approve assignment (HITID:{} AssignmentID:{} workerID: {})".format(hit_id, assignment_id, worker_id))
            if (len(tweet_id_list) != 12) or (len(labels_list) != 12) or (len(tweet_id_list) != len(labels_list)):
                print(hit_id)

    return hit_assignment_ids

def approve_reject_assignments(hit_assignment_ids, MTurk_client, logfile):

    print('Use API to approve/reject assignments:')

    for k, v in hit_assignment_ids.items():
        print(k, len(v))
        for index, assignment_id in enumerate(v):
            # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.get_assignment
            response = MTurk_client.get_assignment(AssignmentId=assignment_id)

            Assignment = response['Assignment']
            WorkerId = Assignment['WorkerId']
            AssignmentStatus = Assignment['AssignmentStatus']
            AutoApprovalTime = datetime2string(Assignment['AutoApprovalTime'])
            ApprovalTime = ''
            RejectionTime = ''
            if 'ApprovalTime' in Assignment:
                ApprovalTime = datetime2string(Assignment['ApprovalTime'])
            if 'RejectionTime' in Assignment:
                RejectionTime = datetime2string(Assignment['RejectionTime'])
            print(index, assignment_id, WorkerId, AssignmentStatus, AutoApprovalTime, ApprovalTime, RejectionTime)

            if AssignmentStatus == 'Submitted':
            # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.approve_assignment
                record = MTurk_client.approve_assignment(AssignmentId=assignment_id)
                print('Approved HIT: %s Worker: %s Assignment: %s at %s' % (k, WorkerId, assignment_id, get_timestamp()))
                logfile.write('Approved HIT: %s Worker: %s Assignment: %s at %s\n' % (k, WorkerId, assignment_id, get_timestamp()))
        print

if __name__ == '__main__':
    user_input = sys.argv[1]

    # Get hit id(s) from log file (.txt)
    if user_input.endswith('.txt'):
        file_name = user_input
        hit_id_list = read_HITs_log(file_name)
        print 'Checking {} HITs......\n'.format(len(hit_id_list))
        print(hit_id_list)
    # Get hid id from command line
    else:
        hit_id = user_input
        hit_id_list = [hit_id]
        print 'Checking HIT {}...\n'.format(hit_id)

    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    hit_collection = db[HIT_COLLECTION]
    label_collection = db[LABEL_COLLECTION]
    print('MongoDB connected\n')

    # hit_assignment_ids = check_database_records(hit_id_list, hit_collection, label_collection)

    MTurk_client = get_client('production')

    with open(get_log_directory('HIT_approve') + '/records.txt', 'a') as logfile:
        for index, hit_id in enumerate(hit_id_list):
            print(index, hit_id)
            MTurk_workers_assignments = check_submissions_MTurk(MTurk_client, hit_id)
            print
            hit_assignment_ids = check_submissions_MongoDB(hit_collection, label_collection, hit_id, MTurk_workers_assignments)
            print
            approve_reject_assignments(hit_assignment_ids, MTurk_client, logfile)
            print('----------------------------------------')