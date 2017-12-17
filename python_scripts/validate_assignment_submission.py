import sys
from pymongo import MongoClient
from helper_functions import get_timestamp, get_log_directory

HIT_COLLECTION = 'hit'
LABEL_COLLECTION = 'label'


def validate(answer1, answer2):
    if answer1['question1'] == answer2['question1'] and answer1['question2'] == answer2['question2']:
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


def get_documents(file_name, hit_collection, label_collection):
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

    for index, hit in enumerate(hit_id_list):
        print(index + "==" + hit + "==")
        for document in hit_collection.find({'hitID': hit}):
            assignment_id = document['assignmentID']
            worker_id = document['workerID']
            tweet_id_list = document['tweetList']

            tweet_id_set = set()

            match_count = 0
            mismatch = 0
            for tweet_id in tweet_id_list:
                if mismatch > 0:
                    print("Reject assignment (HITID:{} AssignmentID:{} workerID: {})".format(hit, assignment_id,
                                                                                            worker_id))
                    break
                result = label_collection.find({'hitID': hit, 'workerID': worker_id, 'assignmentID': assignment_id, 'id': tweet_id})

                if result.count() == 2 and tweet_id not in tweet_id_set:
                    if validate(result[0], result[1]):
                        if validate_q3(result[0], result[1]):
                            match_count += 1
                        else:
                            mismatch += 1
                    else:
                        mismatch += 1

                tweet_id_set.add(tweet_id)
            if mismatch == 0:
                print("Approve assignment (HITID:{} AssignmentID:{} workerID: {})".format(hit, assignment_id, worker_id))
            print


if __name__ == '__main__':
    file_name = sys.argv[1]
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    hit_collection = db[HIT_COLLECTION]
    label_collection = db[LABEL_COLLECTION]
    get_documents(file_name, hit_collection, label_collection)
