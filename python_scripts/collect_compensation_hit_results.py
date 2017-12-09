import sys
import time

from pymongo import MongoClient

from check_hitinfo_payment import get_workerid_assignmentid
from create_compensation_hit import get_client

FEEDBACK_COLLECTION = "compensationHITSubmission"


def is_worker_info_available(worker_id, collection):

    result= collection.find({'workerID': worker_id}).count()
    return False if result == 0 else True


def store_assignement_info_on_submission(client):
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    collection = db[FEEDBACK_COLLECTION]
    while(True):
        time.sleep(5)
        assignment_info = get_workerid_assignmentid(client)

        for worker_id in assignment_info:
            result = is_worker_info_available(worker_id, collection)
            if not result:
                assignment_id = assignment_info[worker_id]['assignmentID']
                feedback = assignment_info[worker_id]['feedback']
                document = {
                    'workerID': worker_id,
                    'assignment_id': assignment_id,
                    'feedback': feedback
                }
                collection.insert_one(document)


def main(environment):
    client = get_client(environment)
    store_assignement_info_on_submission(client)


if __name__ == '__main__':
    environment = sys.argv[1]
    main(environment)