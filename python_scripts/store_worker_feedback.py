from pymongo import MongoClient

FEEDBACK_COLLECTION = "compensationHITInfo"


def store_feedback_in_db(worker_id, assignment_id, feedback):
    mongo_client = MongoClient('localhost', 3001)
    db = mongo_client.meteor
    collection = db[FEEDBACK_COLLECTION]
    document = {
        'workerID': worker_id,
        'assignment_id': assignment_id,
        'feedback': feedback
    }
    collection.insert_one(document)