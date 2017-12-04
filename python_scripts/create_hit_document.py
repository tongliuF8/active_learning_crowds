"""
Creates a document for new HIT created in mturk
"""
from pymongo import MongoClient, ASCENDING, DESCENDING

ACTIVE_TWEET_COLLECTION = "activeTweet"
TWEET_COLLECTION = "oneYearData"

# Will be replaced by query strategy
RANDOM_NUMBER = 10


def insert_document(collection_name, final_collection, hit_id):
    """
    Collects the tweets from text collection and inserts them to the collection used by the meteor application.
    :param collection_name:  collection with job related tweets
    :param final_collection: Collection use by meteor
    :param hit_id: HIT ID
    :return: None
    """
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    collection = db[collection_name]
    final = db[final_collection]
    tweet_list = []

    for document in collection.find().sort([("fitnessFuncValue", DESCENDING)]).skip(RANDOM_NUMBER).limit(10):
        tweet_list.append({
            'id': document['id'],
            'text': document['text'],
            'message_1': 'message-1',
            'message_2': 'message-2',
            'message_3': 'message-3',
            'message1': 'message1',
            'message2': 'message2',
            'message3': 'message3',
            'time_text': 'time_text',
            'time_message_1':'time_message-1',
            'time_message_2': 'time_message-2',
            'time_message_3': 'time_message-3',
            'time_message1': 'time_message1',
            'time_message2': 'time_message2',
            'time_message3': 'time_message3'
        })

    for document in collection.find().sort([("fitnessFuncValue", DESCENDING)]).skip(
                    (collection.find().count()//2) + RANDOM_NUMBER).limit(10):
        tweet_list.append({
            'id': document['id'],
            'text': document['text'],
            'message_1': 'message-1',
            'message_2': 'message-2',
            'message_3': 'message-3',
            'message1': 'message1',
            'message2': 'message2',
            'message3': 'message3',
            'time_text': 'time_text',
            'time_message_1': 'time_message-1',
            'time_message_2': 'time_message-2',
            'time_message_3': 'time_message-3',
            'time_message1': 'time_message1',
            'time_message2': 'time_message2',
            'time_message3': 'time_message3'
        })

    for document in collection.find().sort([("fitnessFuncValue", ASCENDING)]).skip(RANDOM_NUMBER).limit(10):
        tweet_list.append({
            'id': document['id'],
            'text': document['text'],
            'message_1': 'message-1',
            'message_2': 'message-2',
            'message_3': 'message-3',
            'message1': 'message1',
            'message2': 'message2',
            'message3': 'message3',
            'time_text': 'time_text',
            'time_message_1': 'time_message-1',
            'time_message_2': 'time_message-2',
            'time_message_3': 'time_message-3',
            'time_message1': 'time_message1',
            'time_message2': 'time_message2',
            'time_message3': 'time_message3'
        })

    final.insert_one({
        'hitID': hit_id,
        'tweets': tweet_list
    })


def create_document(hit_id):
    """
    Creates a new document with HIT id as key.
    :param hit_id: mturk HIT ID
    :return: None
    """
    insert_document(TWEET_COLLECTION, ACTIVE_TWEET_COLLECTION, hit_id)